import pdfplumber


class PDFReader:
    """
        Lee un PDF y devuelve una representación interna del documento.

        Esta clase NO sabe qué es una glosa.
        Solamente se encarga de leer:
        - texto
        - tablas
        - páginas
    """

    def read(self, file) -> dict:
        # Algunas validaciones/extractores anteriores pueden haber
        # movido el puntero del archivo.
        if hasattr(file, "seek"):
            file.seek(0)

        pages = []

        with pdfplumber.open(file) as pdf:

            for page_number, page in enumerate(
                pdf.pages,
                start=1
            ):

                text = page.extract_text() or ""

                tables = page.extract_tables() or []

                pages.append({
                    "page_number": page_number,
                    "text": text,
                    "tables": tables,
                })

        return {
            "total_pages": len(pages),
            "pages": pages,
        }