from __future__ import annotations

import io
import re
from datetime import datetime
from collections import OrderedDict
from pathlib import Path
from typing import Any

import xlrd
import xlwt
from xlutils.copy import copy as xl_copy


class ExcelExportService:

    # Ruta a la plantilla oficial de la herramienta (la que ella misma
    # exporta para "llenar los datos ahí"). Debe vivir dentro del proyecto,
    # junto a este archivo, en una carpeta "plantillas".
    #
    # Generamos el .xls PARTIENDO de esta plantilla (en vez de construir
    # el libro desde cero con xlwt) para garantizar exactamente el mismo
    # formato BIFF y los mismos estilos/encabezados que la herramienta
    # antigua espera.
    TEMPLATE_PATH = (
        Path(__file__).resolve().parent.parent
        / "templates"
        / "PLANTILLA_INGRESO_GLOSAS_MASIVO.XLS"
    )

    # Índice de cada hoja dentro de la plantilla
    HOJA_FACTURAS_IDX = 0  # FACTURAS_CG
    HOJA_DETALLES_IDX = 1  # DETALLES_CG

    # Columnas que el software antiguo espera como NUMERO en el .xls,
    # el resto siempre se escribe como texto (aunque el valor "parezca"
    # numérico, p. ej. códigos que empiezan en cero).
    CAMPOS_NUMERICOS = {
        "NUMERO_FACTURA",
        "TIPO_FACTURA",
        "VALOR_GLOSADO_TOTAL",
        "VALOR_GLOSA_ITEM",
    }

    FACTURAS_COLUMNS = [
        "NUMERO_FACTURA",
        "TIPO_FACTURA",
        "FECHA_RECEPCION_GLOSA",
        "DEVOLUCION",
        "PUNTO_RUTA_DESTINO",
        "EMPRESA_PUNTO_RUTA_DESTINO",
        "SEDE_PUNTO_RUTA_DESTINO",
        "VALOR_GLOSADO_TOTAL",
    ]

    DETALLES_COLUMNS = [
        "NUMERO_FACTURA",
        "TIPO_FACTURA",
        "CODIGO_GLOSA",
        "TIPO_ITEM",
        "CODIGO_ITEM",
        "CODIGO_HONORARIO",
        "OBSERVACION_RECEPCION_GLOSA",
        "VALOR_GLOSA_ITEM",
        "NUMERO_ORDEN_SERVICIO",
        "TIPO_ORDEN_SERVICIO",
        "OBSERVACION_RESPONSABLE",
    ]

    def generar_excel(self, facturas: list[dict[str, Any]]) -> bytes:
        """
        Genera un único Excel con todas las facturas recibidas.

        Cada factura aporta:
        - Una fila en FACTURAS_CG.
        - Sus items detallados y HIS en DETALLES_CG.
        """

        if not facturas:
            raise ValueError("No se recibieron facturas para exportar.")

        facturas_xls = []
        detalles_xls = []

        for factura in facturas:
            facturas_xls.append(
                self._crear_factura(factura)
            )

            detalles_xls.extend(
                self._crear_detalles(factura)
            )

        facturas_xls = self._normalizar_facturas(facturas_xls)
        detalles_xls = self._normalizar_detalles(detalles_xls)

        return self._generar_excel(
            facturas=facturas_xls,
            detalles=detalles_xls,
        )

    # ============================================================
    # FACTURAS_CG
    # ============================================================

    def _crear_factura(
        self,
        factura: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Construye la fila correspondiente a FACTURAS_CG.

        Equivale a la preparación del encabezado realizada
        actualmente en FastAPI.
        """

        encabezado = factura.get("encabezado") or {}

        numero_factura = encabezado.get(
            "numero_factura",
            factura.get("numero_factura", ""),
        )

        tipo_factura = encabezado.get(
            "tipo_factura",
            factura.get("tipo_factura", ""),
        )

        fecha = self._formatear_fecha(
            encabezado.get("fecha_notificacion", "")
        )

        valor_glosa = self._numero_entero(
            encabezado.get("valor_glosa", 0)
        )

        devolucion = factura.get("devolucion", "N") or "N"

        punto_ruta = factura.get("punto_ruta") or {}

        if devolucion == "S":
            punto_ruta_destino = punto_ruta.get("codigo", "")
            empresa_punto_ruta = punto_ruta.get("empresa", "")

            # Tu frontend usa PuntoRuta.
            # El backend anterior manejaba "sede".
            sede_punto_ruta = (
                punto_ruta.get("sede")
                or punto_ruta.get("departamento")
                or ""
            )
        else:
            punto_ruta_destino = ""
            empresa_punto_ruta = ""
            sede_punto_ruta = ""

        return {
            "NUMERO_FACTURA": self._numero_entero(numero_factura),
            "TIPO_FACTURA": self._numero_entero(tipo_factura),
            "FECHA_RECEPCION_GLOSA": fecha,
            "DEVOLUCION": devolucion,
            "PUNTO_RUTA_DESTINO": punto_ruta_destino,
            "EMPRESA_PUNTO_RUTA_DESTINO": empresa_punto_ruta,
            "SEDE_PUNTO_RUTA_DESTINO": sede_punto_ruta,
            "VALOR_GLOSADO_TOTAL": valor_glosa,
        }

    # ============================================================
    # DETALLES_CG
    # ============================================================

    def _crear_detalles(
        self,
        factura: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Construye todos los detalles de una factura:

        1. Items detallados provenientes del PDF.
        2. Items HIS seleccionados para los globales.
        """

        detalles = []

        detalles.extend(
            self._crear_items_pdf(factura)
        )

        detalles.extend(
            self._crear_items_his(factura)
        )

        return detalles

    # ============================================================
    # ITEMS PDF
    # ============================================================

    def _crear_items_pdf(
        self,
        factura: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Toma los items del PDF y elimina los globales.

        Esta es la misma regla de _es_item_global()
        que actualmente existe en FastAPI.
        """

        encabezado = factura.get("encabezado") or {}

        numero_factura = encabezado.get(
            "numero_factura",
            factura.get("numero_factura", ""),
        )

        tipo_factura = encabezado.get(
            "tipo_factura",
            factura.get("tipo_factura", ""),
        )

        items = factura.get("items") or []

        detalles = []

        for item in items:

            if self._es_item_global(item):
                continue

            detalles.append(
                self._crear_detalle_pdf(
                    numero_factura=numero_factura,
                    tipo_factura=tipo_factura,
                    item=item,
                )
            )

        return detalles

    # ============================================================
    # ITEMS HIS
    # ============================================================

    def _crear_items_his(
        self,
        factura: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Convierte las selecciones HIS de cada global
        al formato utilizado por DETALLES_CG.

        El nuevo frontend ya entrega la relación:

            factura
                └── global
                     └── selecciones_his[]

        Por lo tanto no necesitamos reconstruir la relación
        mediante globalUid.
        """

        encabezado = factura.get("encabezado") or {}

        numero_factura = encabezado.get(
            "numero_factura",
            factura.get("numero_factura", ""),
        )

        tipo_factura = encabezado.get(
            "tipo_factura",
            factura.get("tipo_factura", ""),
        )

        globales = factura.get("globales") or []

        detalles = []

        for global_item in globales:

            selecciones_his = (
                global_item.get("selecciones_his") or []
            )

            for his in selecciones_his:

                detalles.append(
                    self._crear_detalle_his(
                        numero_factura=numero_factura,
                        tipo_factura=tipo_factura,
                        global_item=global_item,
                        his=his,
                    )
                )

        return detalles

    # ============================================================
    # DETALLE PDF
    # ============================================================

    def _crear_detalle_pdf(
        self,
        numero_factura: Any,
        tipo_factura: Any,
        item: dict[str, Any],
    ) -> dict[str, Any]:

        return {
            "NUMERO_FACTURA": self._numero_entero(numero_factura),
            "TIPO_FACTURA": self._numero_entero(tipo_factura),
            "CODIGO_GLOSA": item.get("codigo_glosa", ""),
            "TIPO_ITEM": item.get("tipo_item", ""),
            "CODIGO_ITEM": item.get("codigo_item", ""),
            "CODIGO_HONORARIO": item.get("codigo_honorario", ""),
            "OBSERVACION_RECEPCION_GLOSA": (
                item.get("descripcion_causa")
                or item.get("codigo_glosa")
                or ""
            )[:255],
            "VALOR_GLOSA_ITEM": self._numero_entero(
                item.get("valor_glosa", 0)
            ),
            "NUMERO_ORDEN_SERVICIO": "",
            "TIPO_ORDEN_SERVICIO": "",
            "OBSERVACION_RESPONSABLE": "",
        }

    # ============================================================
    # DETALLE HIS
    # ============================================================

    def _crear_detalle_his(
        self,
        numero_factura: Any,
        tipo_factura: Any,
        global_item: dict[str, Any],
        his: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Replica la transformación que actualmente realiza
        exportar_xls() para cada selección HIS.
        """

        grupo = str(
            his.get("fuente")
            or ""
        )

        # --------------------------------------------------------
        # Causa
        # --------------------------------------------------------
        #
        # Regla actual de FastAPI:
        #
        # MATipP = 5 / quirurg
        #       -> 58
        #
        # cualquier otro
        #       -> 01
        #
        if (
            "MATipP = 5" in grupo
            or "quirurg" in grupo.lower()
        ):
            causa_num = "58"
        else:
            causa_num = "01"

        # --------------------------------------------------------
        # Código de glosa
        # --------------------------------------------------------

        codigo_glosa_raw = (
            global_item.get("codigo_glosa")
            or ""
        )

        codigo_glosa = self._limpiar_codigo_glosa(
            codigo_glosa_raw
        )

        # --------------------------------------------------------
        # Observación
        # --------------------------------------------------------

        descripcion_causa = (
            global_item.get("descripcion_causa")
            or ""
        )

        if descripcion_causa.startswith(codigo_glosa_raw):
            observacion = descripcion_causa

        else:
            observacion = (
                f"{codigo_glosa_raw}. {descripcion_causa}"
                .strip(". ")
                if descripcion_causa
                else codigo_glosa_raw
            )

        # --------------------------------------------------------
        # Valor
        # --------------------------------------------------------

        valor_editado = his.get("valor_editado")

        if valor_editado is not None:
            valor_final = valor_editado

        else:
            valor_final = (
                his.get("valor")
                or his.get("valor_original")
                or 0
            )

        # --------------------------------------------------------
        # Código item
        # --------------------------------------------------------

        codigo_item = (
            his.get("codigo")
            or ""
        )

        # --------------------------------------------------------
        # Código honorario
        # --------------------------------------------------------

        codigo_honorario = (
            his.get("codigo_honorario")
            or ""
        )

        return {
            "NUMERO_FACTURA": self._numero_entero(numero_factura),
            "TIPO_FACTURA": self._numero_entero(tipo_factura),
            "CODIGO_GLOSA": codigo_glosa,
            "TIPO_ITEM": "P",
            "CODIGO_ITEM": codigo_item,
            "CODIGO_HONORARIO": codigo_honorario,
            "OBSERVACION_RECEPCION_GLOSA": observacion[:255],
            "VALOR_GLOSA_ITEM": self._numero_entero(valor_final),
            "NUMERO_ORDEN_SERVICIO": "",
            "TIPO_ORDEN_SERVICIO": "",
            "OBSERVACION_RESPONSABLE": "",
        }

    # ============================================================
    # REGLAS DEL EXPORTADOR ACTUAL
    # ============================================================

    @staticmethod
    def _es_item_global(
        item: dict[str, Any],
    ) -> bool:
        """
        Determina si un item del PDF es global.

        MISMA REGLA QUE EL FASTAPI ACTUAL:

        - es_global=True
        - causa 01
        - causa 58
        - CUPS/CUM vacío
        """

        if item.get("es_global"):
            return True

        causa = item.get(
            "causa_especifica",
            ""
        ) or ""

        match = re.search(
            r"(\d+)",
            str(causa),
        )

        numero_causa = (
            match.group(1).zfill(2)[:2]
            if match
            else ""
        )

        if numero_causa in ("01", "58"):
            return True

        cups = str(
            item.get("codigo_cups_pdf")
            or ""
        ).strip()

        if not cups:
            return True

        return False

    @staticmethod
    def _limpiar_codigo_glosa(
        codigo: Any,
    ) -> str:
        """
        Replica _limpiar_codigo_glosa() de FastAPI.

        Ejemplos:

            16506-CL0601
            -> CL0601

            TA0101
            -> TA0101

            12501-TA0101
            -> TA0101
        """

        if not codigo:
            return ""

        matches = re.findall(
            r"([A-Z]{2}\d{4})",
            str(codigo),
        )

        return (
            matches[-1]
            if matches
            else str(codigo).strip()
        )

    @staticmethod
    def _formatear_fecha(
        fecha: Any,
    ) -> str:
        """
        Convierte las fechas aceptadas por el exportador
        a DD/MM/AAAA.
        """

        if not fecha:
            return ""

        fecha = str(fecha).strip()

        formatos = (
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%d.%m.%Y",
        )

        for formato in formatos:
            try:
                return datetime.strptime(
                    fecha,
                    formato,
                ).strftime("%d/%m/%Y")

            except ValueError:
                continue

        return fecha

    @staticmethod
    def _num_causa(
        causa: Any,
    ) -> str:
        """
        Extrae el número de causa.

        Ejemplo:

            '01 - Estancia'
            -> '01'

            '58 Procedimiento quirúrgico'
            -> '58'
        """

        match = re.search(
            r"(\d+)",
            str(causa or ""),
        )

        return (
            match.group(1).zfill(2)[:2]
            if match
            else ""
        )

    # ============================================================
    # NORMALIZACIÓN
    # ============================================================

    def _normalizar_facturas(
        self,
        facturas: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        return [
            {
                columna: factura.get(
                    columna,
                    "",
                )
                for columna in self.FACTURAS_COLUMNS
            }
            for factura in facturas
        ]

    def _normalizar_detalles(
        self,
        detalles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Replica la agrupación de generar_xls():

        - SIN código de honorario:
            agrupar por CODIGO_ITEM.

        - CON código de honorario:
            mantener individual.

        Se mantiene el orden de primera aparición.
        """

        agrupados = OrderedDict()

        orden = []

        for detalle in detalles:

            codigo_honorario = str(
                detalle.get(
                    "CODIGO_HONORARIO",
                    "",
                )
                or ""
            ).strip()

            # ----------------------------------------------------
            # Tiene honorario -> fila individual
            # ----------------------------------------------------

            if codigo_honorario:

                orden.append(
                    ("individual", detalle)
                )

                continue

            # ----------------------------------------------------
            # Sin honorario -> agrupar
            # ----------------------------------------------------

            clave = (
                detalle.get(
                    "NUMERO_FACTURA",
                    "",
                ),
                detalle.get(
                    "TIPO_FACTURA",
                    "",
                ),
                detalle.get(
                    "CODIGO_GLOSA",
                    "",
                ),
                detalle.get(
                    "TIPO_ITEM",
                    "",
                ),
                str(
                    detalle.get(
                        "CODIGO_ITEM",
                        "",
                    )
                    or ""
                ),
            )

            if clave not in agrupados:

                agrupados[clave] = dict(detalle)

                agrupados[clave][
                    "VALOR_GLOSA_ITEM"
                ] = self._numero_entero(
                    detalle.get(
                        "VALOR_GLOSA_ITEM",
                        0,
                    )
                )

                orden.append(
                    ("agrupado", clave)
                )

            else:

                agrupados[clave][
                    "VALOR_GLOSA_ITEM"
                ] += self._numero_entero(
                    detalle.get(
                        "VALOR_GLOSA_ITEM",
                        0,
                    )
                )

        resultado = []

        claves_ya_agregadas = set()

        for tipo, dato in orden:

            if tipo == "individual":

                resultado.append(dato)

            else:

                if dato in claves_ya_agregadas:
                    continue

                resultado.append(
                    agrupados[dato]
                )

                claves_ya_agregadas.add(dato)

        return resultado

    # ============================================================
    # GENERACIÓN DEL EXCEL
    # ============================================================

    def _generar_excel(
        self,
        facturas: list[dict[str, Any]],
        detalles: list[dict[str, Any]],
    ) -> bytes:
        """
        Genera el .xls final PARTIENDO DE LA PLANTILLA OFICIAL de la
        herramienta (nunca se modifica el archivo original, solo se
        copia en memoria y se llena).

        Antes este método armaba el libro desde cero con xlwt; se
        cambió porque el archivo resultante, aunque era un .xls BIFF
        válido, seguía siendo "demasiado nuevo" para la herramienta.
        Partir de la plantilla real garantiza el mismo formato exacto
        (encabezados, estilos, orden de hojas) que ella exporta.

        Mantiene las dos hojas de siempre:

            FACTURAS_CG
            DETALLES_CG
        """

        if not self.TEMPLATE_PATH.exists():
            raise FileNotFoundError(
                f"No se encontró la plantilla en {self.TEMPLATE_PATH}"
            )

        # 1. Leer la plantilla original (formatting_info=True conserva
        #    encabezados, anchos de columna y estilos).
        libro_plantilla = xlrd.open_workbook(
            str(self.TEMPLATE_PATH),
            formatting_info=True,
        )

        # 2. Copiarla a un libro editable (xlwt) sin perder el formato.
        workbook = xl_copy(libro_plantilla)

        # 3. Escribir los datos a partir de la fila 1 (la 0 es el
        #    encabezado que ya trae la plantilla).
        hoja_facturas = workbook.get_sheet(self.HOJA_FACTURAS_IDX)
        self._escribir_hoja(
            hoja=hoja_facturas,
            columnas=self.FACTURAS_COLUMNS,
            filas=facturas,
        )

        hoja_detalles = workbook.get_sheet(self.HOJA_DETALLES_IDX)
        self._escribir_hoja(
            hoja=hoja_detalles,
            columnas=self.DETALLES_COLUMNS,
            filas=detalles,
        )

        buffer = io.BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        return buffer.getvalue()

    # ============================================================
    # ESCRITURA DE HOJA (tipos de dato)
    # ============================================================

    # def _escribir_hoja(
    #     self,
    #     hoja,
    #     columnas: list[str],
    #     filas: list[dict[str, Any]],
    # ) -> None:
    #     """
    #     Escribe solo las FILAS de datos: el encabezado, los estilos,
    #     el freeze de la primera fila y el ancho de columnas ya vienen
    #     dados por la plantilla, así que no se tocan aquí.

    #     - Columnas en CAMPOS_NUMERICOS -> celda numérica real (int).
    #     - El resto -> celda de texto, incluso si "parece" un número
    #       (para no perder ceros a la izquierda en códigos).
    #     """

    #     for fila_idx, fila in enumerate(filas, start=1):
    #         for columna_idx, nombre_columna in enumerate(columnas):
    #             valor = fila.get(nombre_columna, "")

    #             if nombre_columna in self.CAMPOS_NUMERICOS:
    #                 hoja.write(
    #                     fila_idx,
    #                     columna_idx,
    #                     self._numero_entero(valor),
    #                 )
    #             else:
    #                 hoja.write(
    #                     fila_idx,
    #                     columna_idx,
    #                     "" if valor is None else str(valor),
    #                 )

    def _escribir_hoja(
        self,
        hoja,
        columnas: list[str],
        filas: list[dict[str, Any]],
    ) -> None:
        """
        Escribe las filas de datos respetando los tipos que espera
        el aplicativo antiguo.

        - CAMPOS_NUMERICOS -> número entero real.
        - FECHA_RECEPCION_GLOSA -> fecha real de Excel.
        - CODIGO_ITEM:
            * Solo dígitos -> número.
            * Cualquier otro contenido -> texto.
        - Resto de campos -> texto.
        """

        for fila_idx, fila in enumerate(filas, start=1):
            for columna_idx, nombre_columna in enumerate(columnas):

                valor = fila.get(nombre_columna, "")

                # ----------------------------------------------------
                # CAMPOS NUMÉRICOS
                # ----------------------------------------------------

                if nombre_columna in self.CAMPOS_NUMERICOS:

                    hoja.write(
                        fila_idx,
                        columna_idx,
                        self._numero_entero(valor),
                    )

                # ----------------------------------------------------
                # FECHA_RECEPCION_GLOSA
                # ----------------------------------------------------

                elif nombre_columna == "FECHA_RECEPCION_GLOSA":

                    self._escribir_fecha(
                        hoja,
                        fila_idx,
                        columna_idx,
                        valor,
                    )

                # ----------------------------------------------------
                # CODIGO_ITEM
                # ----------------------------------------------------

                elif nombre_columna == "CODIGO_ITEM":

                    if self._es_codigo_numerico(valor):

                        # Se escribe como NUMERO real en Excel
                        hoja.write(
                            fila_idx,
                            columna_idx,
                            int(str(valor).strip()),
                        )

                    else:

                        # Se escribe como TEXTO
                        hoja.write(
                            fila_idx,
                            columna_idx,
                            "" if valor is None else str(valor),
                        )

                # ----------------------------------------------------
                # RESTO DE CAMPOS
                # ----------------------------------------------------

                else:

                    hoja.write(
                        fila_idx,
                        columna_idx,
                        "" if valor is None else str(valor),
                    )
    # ============================================================
    # UTILIDADES
    # ============================================================
    
    @staticmethod
    def _es_codigo_numerico(
        valor: Any,
    ) -> bool:
        """
        Determina si CODIGO_ITEM debe almacenarse como número.

        Ejemplos:

            901009       -> True
            903813       -> True
            60611520     -> True

            29523-5      -> False
            19979159-2   -> False
            JEPUCA       -> False
            CTIV22       -> False
            ASTRSA       -> False
        """

        if valor is None:
            return False

        texto = str(valor).strip()

        if not texto:
            return False

        return bool(re.fullmatch(r"\d+", texto))
    
    @staticmethod
    def _escribir_fecha(
        hoja,
        fila_idx: int,
        columna_idx: int,
        valor: Any,
    ) -> None:
        """
        Escribe FECHA_RECEPCION_GLOSA como una fecha real de Excel,
        no como texto.

        Acepta fechas en formatos:
            dd/mm/YYYY
            YYYY-mm-dd
            YYYY/mm/dd
            dd-mm-YYYY
            dd.mm.YYYY
        """

        if valor is None or str(valor).strip() == "":
            hoja.write(
                fila_idx,
                columna_idx,
                "",
            )
            return

        fecha = None

        # Si ya recibimos un datetime, lo usamos directamente.
        if isinstance(valor, datetime):
            fecha = valor

        else:
            texto = str(valor).strip()

            formatos = (
                "%d/%m/%Y",
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%d-%m-%Y",
                "%d.%m.%Y",
            )

            for formato in formatos:
                try:
                    fecha = datetime.strptime(
                        texto,
                        formato,
                    )
                    break

                except ValueError:
                    continue

        # Si no pudimos convertirla, la escribimos como texto
        # para no romper la generación del archivo.
        if fecha is None:

            hoja.write(
                fila_idx,
                columna_idx,
                str(valor),
            )

            return

        # Formato de fecha que verá Excel.
        estilo_fecha = xlwt.easyxf(
            num_format_str="dd/mm/yyyy"
        )

        # IMPORTANTE:
        # write_datetime escribe una fecha real de Excel,
        # no una cadena de texto.
        hoja.write(
            fila_idx,
            columna_idx,
            fecha,
            estilo_fecha,
        )

    @staticmethod
    def _numero_entero(
        valor: Any,
    ) -> int:

        if valor is None:
            return 0

        try:
            return int(float(valor))

        except (
            TypeError,
            ValueError,
        ):
            return 0