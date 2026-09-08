import re
from ..extractor.item_classifier import ItemClassifier
from ..repositories.his_repository import HISRepository


class ItemEnrichmentService:

    CAUSAS_BUSCAR_BD = {"07", "61"}

    def __init__(self, repository: HISRepository = None, classifier: ItemClassifier = None):
        self.repository = repository or HISRepository()
        self.classifier = classifier or ItemClassifier()

    def enrich_all(self, items: list[dict], numero_factura: str, tipo_factura: str) -> list[dict]:
        # 1. Clasificar (reglas 1 y 2, sin BD) — se hace primero para
        #    saber exactamente qué códigos SÍ necesitan consultarse.
        clasificados = [self.classifier.classify(item) for item in items]

        # 2. Recolectar códigos únicos que requieren búsqueda en BD.
        pendientes = {
            self._normalizar_may869(item.get("codigo_cups_pdf", ""))
            for item in clasificados
            if not item["es_global"] and self._requiere_bd(item)
        }

        # 3. Una sola consulta batch — nada de N consultas por ítem repetido.
        mapa_codigos = self.repository.buscar_codigos_item_medicamentos(
            list(pendientes), numero_factura, tipo_factura
        )

        # 4. Resolver todo en memoria contra el diccionario ya traído.
        return [self._resolver_item(item, mapa_codigos) for item in clasificados]

    def _requiere_bd(self, item: dict) -> bool:
        cups_norm = self._normalizar_may869(item.get("codigo_cups_pdf", ""))
        num_causa = self._num_causa(item.get("causa_especifica", ""))
        return cups_norm == "MAY869500" or num_causa in self.CAUSAS_BUSCAR_BD

    def _resolver_item(self, item: dict, mapa_codigos: dict[str, str]) -> dict:
        if item["es_global"]:
            return item

        cups_norm = self._normalizar_may869(item.get("codigo_cups_pdf", ""))
        num_causa = self._num_causa(item.get("causa_especifica", ""))

        # Caso 1: MAY869 -> siempre P
        if cups_norm == "MAY869500":
            item["codigo_item"] = mapa_codigos.get(cups_norm, "MAY869500")
            item["tipo_item"] = "P"
            return item

        # Caso 2: causas 07/61 -> buscar en BD
        if num_causa in self.CAUSAS_BUSCAR_BD:
            codigo = mapa_codigos.get(cups_norm)
            if codigo:
                item["codigo_item"] = codigo
                item["tipo_item"] = "S"
            else:
                # BD no encontró nada -> se trata como global
                item["codigo_item"] = cups_norm
                item["tipo_item"] = "S"
                # item["es_global"] = True
                item["es_global"] = False
            return item

        # Caso 3: causas 05, 06 y el resto -> cups directo, tipo 'S'
        item["codigo_item"] = cups_norm
        item["tipo_item"] = "S"
        return item

    def _num_causa(self, causa: str) -> str:
        m = re.search(r"(\d+)", causa or "")
        return m.group(1).zfill(2)[:2] if m else ""

    def _normalizar_may869(self, cups: str) -> str:
        if re.match(r"MAY869", cups or "", re.IGNORECASE):
            return "MAY869500"
        return cups or ""