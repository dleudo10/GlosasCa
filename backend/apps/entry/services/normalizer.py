import re
import unicodedata


class TextNormalizer:

    @staticmethod
    def normalize(text: str) -> str:

        if not text:
            return ""

        text = str(text)

        # Saltos de línea
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Unicode
        text = unicodedata.normalize("NFD", text)

        text = "".join(
            char
            for char in text
            if unicodedata.category(char) != "Mn"
        )

        # Mayúsculas
        text = text.upper()

        # Espacios
        text = re.sub(r"[ \t]+", " ", text)

        # Espacios alrededor de saltos
        text = re.sub(r" *\n *", "\n", text)

        return text.strip()

    @staticmethod
    def normalize_for_search(text: str) -> str:

        text = TextNormalizer.normalize(text)

        text = text.replace("\n", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def normalize_table(table):

        return [
            [
                TextNormalizer.normalize_for_search(cell or "")
                for cell in row
            ]
            for row in table
        ]