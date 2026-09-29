# import re
# from ..extractor.item_classifier import ItemClassifier
# from ..repositories.his_repository import HISRepository


# class ItemEnrichmentService:

#     CAUSAS_BUSCAR_BD = {"07", "61"}

#     def __init__(self, repository: HISRepository = None, classifier: ItemClassifier = None):
#         self.repository = repository or HISRepository()
#         self.classifier = classifier or ItemClassifier()

#     def enrich_all(self, items: list[dict], numero_factura: str, tipo_factura: str) -> list[dict]:
#         # 1. Clasificar (reglas 1 y 2, sin BD) — se hace primero para
#         #    saber exactamente qué códigos SÍ necesitan consultarse.
#         clasificados = [self.classifier.classify(item) for item in items]

#         # 2. Recolectar códigos únicos que requieren búsqueda en BD.
#         pendientes = {
#             self._normalizar_may869(item.get("codigo_cups_pdf", ""))
#             for item in clasificados
#             if not item["es_global"] and self._requiere_bd(item)
#         }

#         # 3. Una sola consulta batch — nada de N consultas por ítem repetido.
#         mapa_codigos = self.repository.buscar_codigos_item_medicamentos(
#             list(pendientes), numero_factura, tipo_factura
#         )

#         # 4. Resolver todo en memoria contra el diccionario ya traído.
#         return [self._resolver_item(item, mapa_codigos) for item in clasificados]

#     # def _requiere_bd(self, item: dict) -> bool:
#     #     cups_norm = self._normalizar_may869(item.get("codigo_cups_pdf", ""))
#     #     num_causa = self._num_causa(item.get("causa_especifica", ""))
#     #     return cups_norm == "MAY869500" or num_causa in self.CAUSAS_BUSCAR_BD
    
#     _CODIGO_VALIDO_BD_RE = re.compile(r"^\d+$")  # ajusta según el formato real de tus CUPS/CUM

#     def _requiere_bd(self, item: dict) -> bool:
#         cups_norm = self._normalizar_may869(item.get("codigo_cups_pdf", ""))
#         num_causa = self._num_causa(item.get("causa_especifica", ""))
        
#         if cups_norm != "MAY869500" and not self._CODIGO_VALIDO_BD_RE.match(cups_norm):
#             return False  # código no numérico -> no consultar BD, se resuelve como caso 3
        
#         return cups_norm == "MAY869500" or num_causa in self.CAUSAS_BUSCAR_BD

#     def _resolver_item(self, item: dict, mapa_codigos: dict[str, str]) -> dict:
#         if item["es_global"]:
#             return item

#         cups_norm = self._normalizar_may869(item.get("codigo_cups_pdf", ""))
#         num_causa = self._num_causa(item.get("causa_especifica", ""))

#         # Caso 1: MAY869 -> siempre P
#         if cups_norm == "MAY869500":
#             item["codigo_item"] = mapa_codigos.get(cups_norm, "MAY869500")
#             item["tipo_item"] = "P"
#             return item

#         # Caso 2: causas 07/61 -> buscar en BD
#         if num_causa in self.CAUSAS_BUSCAR_BD:
#             codigo = mapa_codigos.get(cups_norm)
#             if codigo:
#                 item["codigo_item"] = codigo
#                 item["tipo_item"] = "S"
#             else:
#                 # BD no encontró nada -> se trata como global
#                 item["codigo_item"] = cups_norm
#                 item["tipo_item"] = "S"
#                 # item["es_global"] = True
#                 item["es_global"] = False
#             return item

#         # Caso 3: causas 05, 06 y el resto -> cups directo, tipo 'S'
#         item["codigo_item"] = cups_norm
#         item["tipo_item"] = "S"
#         return item

#     def _num_causa(self, causa: str) -> str:
#         m = re.search(r"(\d+)", causa or "")
#         return m.group(1).zfill(2)[:2] if m else ""

#     def _normalizar_may869(self, cups: str) -> str:
#         if re.match(r"MAY869", cups or "", re.IGNORECASE):
#             return "MAY869500"
#         return cups or ""
    

import re

from ..extractor.item_classifier import ItemClassifier
from ..repositories.his_repository import HISRepository


class ItemEnrichmentService:

    def __init__(
        self,
        repository: HISRepository = None,
        classifier: ItemClassifier = None,
    ):
        self.repository = repository or HISRepository()
        self.classifier = classifier or ItemClassifier()

    def enrich_all(
        self,
        items: list[dict],
        numero_factura: str,
        tipo_factura: str,
    ) -> list[dict]:

        # ============================================================
        # 1. Clasificar los items
        #
        # Esto mantiene intacta la lógica de globales.
        # ============================================================

        clasificados = [
            self.classifier.classify(item)
            for item in items
        ]

        # ============================================================
        # 2. Obtener todos los CUPS de los items NO globales
        #
        # Ya NO dependemos de:
        #   - causa 07
        #   - causa 61
        #   - MAY869
        #
        # La base de datos será quien determine si el código
        # corresponde realmente a un suministro.
        # ============================================================

        pendientes = {
            self._normalizar_may869(
                item.get("codigo_cups_pdf", "")
            )
            for item in clasificados
            if not item.get("es_global")
            and self._normalizar_may869(
                item.get("codigo_cups_pdf", "")
            )
        }

        # ============================================================
        # 3. Buscar suministros en HIS
        #
        # El método devuelve únicamente coincidencias reales de:
        #
        #     GN_RMS.RMSCUM
        #             ↓
        #     MAEATE3.MSRESO
        #
        # Si no existe coincidencia, NO se agrega el CUPS al mapa.
        # ============================================================

        mapa_codigos = self.repository.buscar_codigos_item_medicamentos(
            list(pendientes),
            numero_factura,
            tipo_factura,
        )

        # ============================================================
        # 4. Resolver los códigos en memoria
        # ============================================================

        return [
            self._resolver_item(item, mapa_codigos)
            for item in clasificados
        ]

    def _resolver_item(
        self,
        item: dict,
        mapa_codigos: dict[str, str],
    ) -> dict:

        # ============================================================
        # GLOBAL
        #
        # No tocar los items globales.
        # ============================================================

        if item.get("es_global"):
            return item

        # ============================================================
        # Código CUPS proveniente del PDF
        # ============================================================

        cups_norm = self._normalizar_may869(
            item.get("codigo_cups_pdf", "")
        )

        # ============================================================
        # Código de item proveniente del PDF
        #
        # Este puede ser, por ejemplo, un CUM u otro código
        # que ya venga en la columna correspondiente del PDF.
        # ============================================================

        codigo_item_pdf = self._normalizar_codigo(
            item.get("codigo_item", "")
        )

        # ============================================================
        # Si no tenemos ningún código, no hacemos nada.
        # ============================================================

        if not cups_norm and not codigo_item_pdf:
            return item

        # ============================================================
        # CASO 1
        #
        # El CUPS está relacionado con MAEATE3.
        #
        # Esto significa que es un suministro/medicamento.
        #
        # CODIGO_ITEM debe ser el MSRESO real.
        # ============================================================

        codigo_suministro = mapa_codigos.get(cups_norm)

        if codigo_suministro:
            item["codigo_item"] = codigo_suministro

            # Esta información puede ser utilizada por otras partes
            # del flujo antes de llegar al Excel.
            item["tipo_item"] = "S"

            return item

        # ============================================================
        # CASO 2
        #
        # No existe en MAEATE3.
        #
        # Por lo tanto NO lo vamos a convertir artificialmente
        # en suministro.
        #
        # Si el PDF ya trae codigo_item_pdf, lo conservamos.
        # Esto permite conservar el CUM u otro código del documento.
        # ============================================================

        if codigo_item_pdf:
            item["codigo_item"] = codigo_item_pdf
        else:
            # Si el PDF no trae código de item, usamos el CUPS.
            item["codigo_item"] = cups_norm

        return item

    def _normalizar_codigo(self, codigo: str) -> str:
        """
        Normaliza un código conservando únicamente su representación
        textual sin espacios innecesarios.
        """

        if not codigo:
            return ""

        codigo = str(codigo).strip()

        codigo = re.sub(
            r"\s+",
            "",
            codigo,
        )

        return codigo

    def _normalizar_may869(self, cups: str) -> str:
        """
        Normaliza las variantes de MAY869 encontradas en el PDF.

        IMPORTANTE:
        MAY869 NO determina por sí solo que el item sea P.
        Únicamente se normaliza el código para poder buscarlo.
        """

        cups = self._normalizar_codigo(cups)

        if re.match(
            r"^MAY869",
            cups,
            re.IGNORECASE,
        ):
            return "MAY869500"

        return cups