import re


class ItemClassifier:
    """
    Determina si un item es 'global' (excluyente) basándose
    únicamente en lo que ya se extrajo del PDF. No consulta BD.

    Un item es global cuando el valor glosado no corresponde a
    un ítem facturado individual identificable, sino a un concepto
    agregado (estancia, procedimiento quirúrgico) que en el HIS
    está compuesto por múltiples líneas.
    """

    CAUSAS_GLOBALES = {"01", "58"}

    def classify(self, item: dict) -> dict:
        item = dict(item)
        item["es_global"] = self._es_global_por_pdf(item)
        item["codigo_glosa"] = self._derivar_codigo_glosa(item)
        return item

    def _es_global_por_pdf(self, item: dict) -> bool:
        cups = (item.get("codigo_cups_pdf") or "").strip()
        # ITEMS GLOBALES
        # if not cups:
        #     return True
        # if self._num_causa(item.get("causa_especifica", "")) in self.CAUSAS_GLOBALES:
        #     return True
        # return False
        return not cups
    
    def _derivar_codigo_glosa(self, item: dict) -> str:
        """
        'TA0701. Los cargos por medicamentos...' -> 'TA0701'
        Si no hay match en el texto, se arma un código de respaldo con
        el prefijo de causa_general + el número de causa específica.
        """
        descripcion_causa = item.get("descripcion_causa", "") or ""
        matches = re.findall(r"([A-Z]{2}\d{4})", descripcion_causa)
        if matches:
            return matches[-1]

        causa_general = (item.get("causa_general", "") or "").strip()
        prefijo_match = re.match(r"([A-Z]{2})", causa_general)
        prefijo = prefijo_match.group(1) if prefijo_match else "NA"
        num_causa = self._num_causa(item.get("causa_especifica", "")) or "00"
        return f"{prefijo}{num_causa}01"

    def _num_causa(self, causa: str) -> str:
        m = re.search(r"(\d+)", causa or "")
        return m.group(1).zfill(2)[:2] if m else ""