import re


class ValueParser:
    """
    Convierte valores extraídos del PDF a tipos consistentes.
    """

    @staticmethod
    def money(value) -> int:

        if value is None:
            return 0

        value = str(value).strip()

        if not value:
            return 0

        value = value.replace("$", "")
        value = value.replace(" ", "")

        # Caso colombiano:
        #
        # 4.733.047,00
        # 4.733.047
        #
        # En ambos casos queremos:
        #
        # 4733047

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

    @staticmethod
    def text(value) -> str:

        if value is None:
            return ""

        return str(value).strip()