from django.db import connections
import re

class HISRepository:
    """
    Acceso de solo lectura al HIS (BD 'clinica') vía el cursor que
    administra Django. Django se encarga de la conexión y del pool;
    aquí solo escribimos SQL — no se usa el query builder del ORM
    porque son joins ya validados contra el esquema legado.
    """

    ALIAS = "clinica"
    
    def buscar_codigos_item_medicamentos(self,
        cups_list: list[str],
        numero_factura: str,
        tipo_factura: str,
    ) -> dict[str, str]:
        if not cups_list:
            return {}

        cups_unicos = sorted({
            str(c).strip()
            for c in cups_list
            if c and str(c).strip()
        })

        if not cups_unicos:
            return {}

        resultado: dict[str, str] = {}

        with connections[self.ALIAS].cursor() as cur:

            # ============================================================
            # PASO 1 — MISMA CONSULTA PRINCIPAL DEL MÉTODO ORIGINAL
            # ============================================================

            placeholders = ", ".join(
                ["%s"] * len(cups_unicos)
            )

            cur.execute(
                f"""
                SELECT
                    GN_RMS.RMSCUM,
                    GN_RMS.RMSMSRESO
                FROM MAEATE3
                INNER JOIN GN_RMS
                    ON MAEATE3.MSRESO = GN_RMS.RMSMSRESO
                WHERE MAEATE3.MPNFac = %s
                AND MAEATE3.MATipDoc = %s
                AND GN_RMS.RMSCUM IN ({placeholders})
                """,
                [
                    numero_factura,
                    str(tipo_factura),
                    *cups_unicos,
                ],
            )

            filas = cur.fetchall()

            for cups, codigo in filas:

                # Equivalente a:
                #
                # if row and row[0] and str(row[0]).strip():

                if not codigo:
                    continue

                cups_key = str(cups).strip()
                codigo_item = str(codigo).strip()

                if not codigo_item:
                    continue

                resultado[cups_key] = codigo_item

            # ============================================================
            # PASO 2 — MISMO FALLBACK DEL MÉTODO ORIGINAL
            #
            # SELECT TOP 1 RMSMSRESO
            # FROM GN_RMS
            # WHERE RMSCUM=?
            # AND RMSMSRESO IS NOT NULL
            # AND RMSMSRESO<>''
            #
            # La única diferencia es que ahora hacemos todos los faltantes
            # mediante IN (...).
            # ============================================================

            faltantes = [
                cups
                for cups in cups_unicos
                if cups not in resultado
            ]

            if faltantes:

                placeholders_fb = ", ".join(
                    ["%s"] * len(faltantes)
                )

                cur.execute(
                    f"""
                    SELECT
                        RMSCUM,
                        RMSMSRESO
                    FROM GN_RMS
                    WHERE RMSCUM IN ({placeholders_fb})
                    AND RMSMSRESO IS NOT NULL
                    AND RMSMSRESO <> ''
                    """,
                    faltantes,
                )

                filas_fallback = cur.fetchall()

                for cups, codigo in filas_fallback:

                    if not codigo:
                        continue

                    cups_key = str(cups).strip()
                    codigo_item = str(codigo).strip()

                    if not codigo_item:
                        continue

                    # Equivalente a que el método original encontró
                    # el primer resultado válido para ese CUPS.
                    if cups_key not in resultado:
                        resultado[cups_key] = codigo_item

            # ============================================================
            # PASO 3 — MISMO COMPORTAMIENTO FINAL DEL MÉTODO ORIGINAL
            #
            # Si no encontró nada:
            #
            #     _cache[key] = cups
            #     return cups
            #
            # Ahora:
            #
            #     resultado[cups] = cups
            # ============================================================

            for cups in cups_unicos:

                if cups not in resultado:

                    resultado[cups] = cups

        return resultado

    def obtener_items_factura(
        self,
        numero_factura: str,
        tipo_factura: str,
        codigos_excluir: list[str] | None = None,
    ) -> list[dict]:
        """
        Ítems de MAEATE2 con nombre (PrNomb) y categoría (TiPrDes),
        excluyendo los códigos ya detallados en el PDF. Alimenta el
        modal de selección de faltantes.
        """
        codigos_excluir = {c.upper().strip() for c in (codigos_excluir or []) if c}

        with connections[self.ALIAS].cursor() as cur:
            cur.execute(
                """
                SELECT
                    MAEATE2.PRCODI,
                    ISNULL(MAEPRO.PrNomb, MAEATE2.PRCODI) AS PrNomb,
                    ISNULL(TIPPROC.TiPrDes, 'Sin categoría') AS TiPrDes,
                    MAEATE2.MAVaTP,
                    MAEATE2.MAHONCOD,
                    MAEATE2.MATipP
                FROM MAEATE2
                LEFT JOIN MAEPRO  ON MAEPRO.PRCODI   = MAEATE2.PRCODI
                LEFT JOIN TIPPROC ON TIPPROC.TiPrCod = MAEPRO.TpPrCd
                WHERE MAEATE2.MATipDoc  = %s
                  AND MAEATE2.MPNFac    = %s
                  AND (MAEATE2.MaEsAnuP <> 'S' OR MAEATE2.MaEsAnuP IS NULL)
                  AND MAEATE2.FcPTpoTrn = 'F'
                ORDER BY TIPPROC.TiPrDes, MAEATE2.PRCODI
                """,
                [str(tipo_factura), str(numero_factura)],
            )
            rows = cur.fetchall()

        resultado = []
        for idx, row in enumerate(rows):
            prcodi   = str(row[0] or "").strip()
            prnomb   = str(row[1] or prcodi).strip()
            tiprdes  = str(row[2] or "Sin categoría").strip()
            mavato   = int(row[3]) if row[3] is not None else 0
            mahoncod = str(row[4] or "").strip()
            matipp   = str(row[5] or "").strip()

            if not prcodi or mavato <= 0:
                continue
            if prcodi.upper() in codigos_excluir:
                continue

            resultado.append({
                "_rownum":          idx,
                "categoria":        tiprdes,
                "codigo_item":      prcodi,
                "codigo_honorario": mahoncod,
                "descripcion":      prnomb,
                "valor":            mavato,
                "fuente":           f"MAEATE2-MATipP{matipp}",
                "tipo_item":        "P",
            })

        return resultado
    
    def _normalizar_codigo(self, value: str) -> str:
        return re.sub(r"\s+", "", str(value or "").strip())
        
    def obtener_puntos_ruta(self) -> list[dict]:
        """
        SELECT PUNRUTCOD, EMPCOD, PUNRUTDES, MCDPTO FROM PUNRUT WHERE PUNRUTEST = 'A'
        """
        with connections[self.ALIAS].cursor() as cur:
            cur.execute("SELECT PUNRUTCOD, EMPCOD, PUNRUTDES, MCDPTO FROM PUNRUT WHERE PUNRUTEST = 'A'")
            rows = cur.fetchall()
            
        return [
            {
                "codigo": str(row[0] or "").strip(),
                "empresa": str(row[1] or "").strip(),
                "descripcion": str(row[2] or "").strip(),
                "departamento": str(row[3] or "").strip(),
            }
            for row in rows
        ]
    
    
      