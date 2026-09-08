import magic


class PDFValidation:

    @staticmethod
    def execute(file):
        if not file.name:
            return {
                "valid": False,
                "error": "El archivo no tiene nombre."
            }

        if not file.name.lower().endswith(".pdf"):
            return {
                "valid": False,
                "error": "El archivo debe tener extensión .pdf."
            }

        if file.size == 0:
            return {
                "valid": False,
                "error": "El archivo está vacío."
            }

        # Validar estructura básica del PDF
        file.seek(0)
        header = file.read(5)
        file.seek(0)

        if header != b"%PDF-":
            return {
                "valid": False,
                "error": "El archivo no tiene una estructura PDF válida."
            }

        # Validar MIME real
        if not PDFValidation._is_pdf(file):
            return {
                "valid": False,
                "error": "El archivo no es un PDF válido."
            }

        return {
            "valid": True,
            "error": None
        }

    @staticmethod
    def _is_pdf(file) -> bool:
        """
            Determina el tipo real del archivo utilizando libmagic.
        """
        try:
            file.seek(0)

            content = file.read(2048)

            file.seek(0)

            mime_type = magic.from_buffer(
                content,
                mime=True
            )

            return mime_type == "application/pdf"

        except Exception:
            return False
