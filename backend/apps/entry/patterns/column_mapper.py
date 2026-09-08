from ..services.normalizer import TextNormalizer

class ColumnMapper:

    ALIASES = {
        "codigo_cups_pdf": [
            "CODIGO CUPS", "CODIGO CUPS/CUM", "CUPS", "CUM",
            "CUPS/CUM", "CODIGO CUPS CUM", "CODIGO",
        ],
        "codigo_item": [
            "CODIGO ITEM", "CODIGO DEL ITEM", "CODIGO ITEM XLS",
            "ITEM", "COD ITEM",
        ],
        "descripcion": [
            "DESCRIPCION", "DESCRIPCION DEL SERVICIO", "DESCRIPCION SERVICIO",
            "DETALLE", "DETALLE DEL SERVICIO", "NOMBRE DEL SERVICIO", "SERVICIO",
        ],
        "tipo_item": ["TIPO", "TIPO ITEM", "TIPO DE ITEM"],
        "valor_cobrado": [
            "VALOR COBRADO", "VALOR FACTURADO", "VALOR DEL SERVICIO",
            "VALOR SERVICIO", "VALOR COBRADO AL PACIENTE",
        ],
        "valor_glosa": [
            "VALOR GLOSA", "VALOR DE GLOSA", "VALOR GLOSADO", "VALOR GLOSA APROBADO",
        ],
        "codigo_glosa": ["CODIGO GLOSA", "COD GLOSA", "COD. GLOSA"],
        "causa_general": ["CAUSA GENERAL", "CAUSA"],
        "causa_especifica": ["CAUSA ESPECIFICA", "CAUSA ESPECÍFICA", "CAUSA ESPECIF"],
        "descripcion_causa": [
            "DETALLE CAUSA", "DESCRIPCION CAUSA", "DESCRIPCIÓN CAUSA",
            "DETALLE DE LA CAUSA", "OBSERVACION", "OBSERVACIONES",
            "DESCRIPCION",  # <- fallback: cuando la columna se llama solo "Descripción"
        ],
    }

    @staticmethod
    def _key(text: str) -> str:
        """Normaliza y además quita TODOS los espacios, para que
        '\n' -> ' ' insertado por normalize_for_search no rompa el match
        (ej: 'CODIGO CUPS/ CUM' vs 'CODIGO CUPS/CUM')."""
        return TextNormalizer.normalize_for_search(text or "").replace(" ", "")

    def map(self, headers: list) -> dict:
        keys = [self._key(h) for h in headers]
        column_map = {}

        for field, aliases in self.ALIASES.items():
            alias_keys = {self._key(a) for a in aliases}
            for index, key in enumerate(keys):
                if key and key in alias_keys and index not in column_map.values():
                    column_map[field] = index
                    break

        return column_map

    def has_item_columns(self, column_map: dict) -> bool:
        important_fields = {"codigo_cups_pdf", "descripcion", "valor_glosa"}
        matches = important_fields.intersection(column_map.keys())
        return len(matches) >= 2

    def compact_indices(self, headers: list) -> list[int]:
        """
        Índices de las columnas cuyo encabezado NO está vacío.
        pdfplumber a veces agrega columnas 'fantasma' (None) solo en
        la página donde detecta el header, y esas columnas desaparecen
        en las páginas de continuación. Compactamos usando el header
        como referencia para que el mapeo de índices coincida con las
        filas de páginas siguientes.
        """
        return [i for i, h in enumerate(headers) if (h or "").strip()]