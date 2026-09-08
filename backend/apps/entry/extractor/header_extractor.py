import re


class HeaderExtractor:
    """
    Extrae información del encabezado de una glosa.

    Recibe el documento previamente procesado por PDFReader.
    No abre directamente el PDF.
    """

    def extract(self, document: dict) -> dict:

        pages = document.get("pages", [])

        if not pages:
            return {}

        text = pages[0].get("text", "")

        return self._extract_from_text(text)

    def _extract_from_text(self, text: str) -> dict:

        result = {}

        result["numero_glosa"] = (
            self._extract_numero_glosa(text)
        )

        result["fecha_notificacion"] = (
            self._extract_fecha(
                text,
                [
                    r"Fecha\s+Notificaci[oó]n",
                ]
            )
        )

        result["fecha_radicacion"] = (
            self._extract_fecha(
                text,
                [
                    r"Fecha\s+Radicaci[oó]n",
                ]
            )
        )

        result["valor_glosa_raw"] = (
            self._extract_money(
                text,
                r"Valor\s+de\s+Glosa"
            )
        )

        result["valor_glosa"] = (
            self._parse_money(
                result["valor_glosa_raw"]
            )
        )

        result["valor_facturado_raw"] = (
            self._extract_money(
                text,
                r"Valor\s+Facturado"
            )
        )

        result["valor_facturado"] = (
            self._parse_money(
                result["valor_facturado_raw"]
            )
        )

        factura = self._extract_factura(text)

        result.update(factura)

        return result

    def _extract_numero_glosa(self, text: str) -> str:

        pattern = (
            r"N[uú]mero\s+de\s+Glosa"
            r"\s+"
            r"(\d+)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return ""

    def _extract_fecha(
        self,
        text: str,
        labels: list[str]
    ) -> str:

        for label in labels:

            pattern = (
                rf"{label}"
                r"\s+"
                r"("
                r"\d{4}/\d{2}/\d{2}"
                r"|"
                r"\d{2}/\d{2}/\d{4}"
                r")"
                r"(?:\s+\d{2}:\d{2}:\d{2})?"
            )

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1)

        return ""

    def _extract_money(
        self,
        text: str,
        label: str
    ) -> str:

        pattern = (
            rf"{label}"
            r"\s*"
            r"\$?\s*"
            r"([\d.,]+)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return ""

    def _parse_money(self, value: str) -> int:

        if not value:
            return 0

        value = str(value).strip()

        value = value.replace("$", "")
        value = value.replace(" ", "")

        # Ejemplo:
        # 4.733.047,00
        if re.search(r",\d{2}$", value):

            value = value[
                :value.rfind(",")
            ]

        value = re.sub(
            r"[^\d]",
            "",
            value
        )

        return int(value) if value else 0

    def _extract_factura(self, text: str) -> dict:

        result = {
            "factura_raw": "",
            "tipo_factura": "",
            "numero_factura": "",
        }

        pattern = (
            r"Factura"
            r"\s+"
            r"((?:SS|SN)"
            r"\s*-\s*"
            r"\d+)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if not match:
            return result

        raw = match.group(1).strip()

        result["factura_raw"] = raw

        tipo = raw.upper().replace(" ", "")

        if tipo.startswith("SS"):
            result["tipo_factura"] = "2"

        elif tipo.startswith("SN"):
            result["tipo_factura"] = "5"

        number_match = re.search(
            r"(\d+)\s*$",
            raw
        )

        if number_match:

            result["numero_factura"] = (
                number_match.group(1)
            )

        return result