from ..patterns.column_mapper import ColumnMapper
from .value_parser import ValueParser
from ..services.normalizer import TextNormalizer
import re

class ItemExtractor:
    """
    Extrae items de las tablas encontradas en un documento PDF.

    Responsabilidades:
    - recorrer todas las páginas
    - detectar tablas candidatas
    - detectar encabezados
    - identificar columnas
    - reutilizar el esquema de columnas entre páginas
    - extraer filas
    - normalizar valores

    NO consulta la base de datos.
    """
    _WS_RE = re.compile(r"\s+")
    _CAUSA_RE = re.compile(r"^\d{1,2}\s*-")

    def __init__(self):
        self.column_mapper = ColumnMapper()
        
    def _limpiar_codigo(self, valor: str) -> str:
        if not valor:
            return ""

        codigo = str(valor).strip()

        # Eliminar saltos y espacios internos
        codigo = re.sub(r"\s+", "", codigo)

        # Eliminar sufijo -CUMxx cuando exista
        codigo = re.sub(
            r"-CUM\d+$",
            "",
            codigo,
            flags=re.IGNORECASE,
        )

        return codigo
        
    def extract(self, document: dict) -> list[dict]:
        items = []
        pages = document.get("pages", [])

        current_column_map = None
        current_keep_indices = None

        for page in pages:
            page_number = page.get("page_number")
            for table_index, table in enumerate(page.get("tables", []), start=1):
                if not table:
                    continue

                result = self._process_table(
                    table=table,
                    page_number=page_number,
                    current_column_map=current_column_map,
                    current_keep_indices=current_keep_indices,
                )
                if result is None:
                    continue

                page_items, detected_column_map, detected_keep_indices = result
                items.extend(page_items)

                if detected_column_map is not None:
                    current_column_map = detected_column_map
                    current_keep_indices = detected_keep_indices

        return items
    
    def _process_table(self, table, page_number, current_column_map, current_keep_indices=None):
        normalized_table = self._normalize_table(table)
        if not normalized_table:
            return None

        header_index = self._find_header_row(normalized_table)

        if header_index is not None:
            raw_headers = normalized_table[header_index]
            keep_indices = self.column_mapper.compact_indices(raw_headers)
            compact_headers = [raw_headers[i] for i in keep_indices]

            column_map = self.column_mapper.map(compact_headers)

            if not self.column_mapper.has_item_columns(column_map):
                return None

            rows = normalized_table[header_index + 1:]
            items = self._extract_rows(
                rows=rows,
                column_map=column_map,
                page_number=page_number,
                keep_indices=keep_indices,
                raw_header_len=len(raw_headers),
            )
            return items, column_map, keep_indices

        if current_column_map is None or not self.column_mapper.has_item_columns(current_column_map):
            return None

        # Nueva guarda: si la tabla no tiene el ancho mínimo esperado para
        # el mapeo de columnas activo, no es una continuación válida.
        max_index_needed = max(current_column_map.values())
        filas_compatibles = [
            row for row in normalized_table
            if len(row) > max_index_needed
        ]
        if not filas_compatibles:
            return None

        items = self._extract_rows(
            rows=filas_compatibles,
            column_map=current_column_map,
            page_number=page_number,
            keep_indices=current_keep_indices,
            raw_header_len=None,
        )
        return items, None, None


    def _extract_rows(self, rows, column_map, page_number, keep_indices=None, raw_header_len=None):
        items = []
        for row_index, row in enumerate(rows):
            compact_row = self._compact_row(row, keep_indices, raw_header_len)
            item = self._extract_item(
                row=compact_row,
                column_map=column_map,
                page_number=page_number,
                row_number=row_index + 1,
            )
            if item is not None:
                items.append(item)
        return items


    def _compact_row(self, row, keep_indices, raw_header_len):
        """
        Solo compacta si la fila viene con la misma longitud 'cruda' que
        tenía el header (misma tabla/página donde se detectó). Las filas
        de páginas de continuación ya llegan compactas de pdfplumber,
        así que se dejan tal cual.
        """
        if not keep_indices or raw_header_len is None or len(row) != raw_header_len:
            return row
        return [row[i] if i < len(row) else "" for i in keep_indices]

    def _normalize_table(self, table) -> list[list[str]]:

        result = []

        for row in table:

            if not row:
                continue

            # Eliminar celdas "fantasma": pdfplumber a veces agrega
            # columnas en None por líneas de la tabla que varían de una
            # página a otra (ej. 16 columnas en la pág. 1, 11 en la pág. 2-3,
            # 12 en la pág. 4 con un None en una posición distinta cada vez).
            # None = ruido estructural. '' = dato real pero vacío (ej. una
            # causa sin descripción) — eso SÍ se debe conservar.
            cleaned_row = [cell for cell in row if cell is not None]

            normalized_row = [
                TextNormalizer.normalize_for_search(cell or "")
                for cell in cleaned_row
            ]

            if not any(normalized_row):
                continue

            result.append(normalized_row)

        return result

    def _find_header_row(
        self,
        table
    ) -> int | None:

        for index, row in enumerate(table):

            column_map = self.column_mapper.map(
                row
            )

            if self.column_mapper.has_item_columns(
                column_map
            ):
                return index

        return None

    def _extract_item(
        self,
        row: list[str],
        column_map: dict,
        page_number,
        row_number,
    ) -> dict | None:

        if not row:
            return None

        def get(field):

            index = column_map.get(field)

            if index is None:
                return ""

            if index >= len(row):
                return ""

            return row[index]

        # codigo_cups = get(
        #     "codigo_cups_pdf"
        # )
        
        codigo_cups = self._limpiar_codigo(
            get("codigo_cups_pdf")
        )

        codigo_item = self._limpiar_codigo(
            get("codigo_item_pdf")
        )

        descripcion = get(
            "descripcion"
        )

        tipo_item = get(
            "tipo_item"
        )

        valor_cobrado = ValueParser.money(
            get("valor_cobrado")
        )

        valor_glosa = ValueParser.money(
            get("valor_glosa")
        )

        codigo_glosa = get(
            "codigo_glosa"
        )

        causa_general = get(
            "causa_general"
        )

        causa_especifica = get(
            "causa_especifica"
        )

        descripcion_causa = get(
            "descripcion_causa"
        )

        # ==================================================
        # Validar si realmente es una fila de item
        # ==================================================

        if not self._is_item_row(
            codigo_cups=codigo_cups,
            codigo_item=codigo_item,
            descripcion=descripcion,
            valor_cobrado=valor_cobrado,
            valor_glosa=valor_glosa,
            causa_especifica=causa_especifica
        ):
            return None

        return {
            "codigo_cups_pdf": codigo_cups,
            "codigo_item": codigo_item,
            "descripcion": descripcion,
            "tipo_item": tipo_item,
            "valor_cobrado": valor_cobrado,
            "valor_glosa": valor_glosa,
            "codigo_glosa": codigo_glosa,
            "causa_general": causa_general,
            "causa_especifica": causa_especifica,
            "descripcion_causa": descripcion_causa,

            # Información técnica.
            "_page": page_number,
            "_row": row_number,
        }

    def _is_item_row(self, codigo_cups, codigo_item, descripcion,
                      valor_cobrado, valor_glosa, causa_especifica=""):
        if valor_glosa <= 0:
            return False
        if not any([codigo_cups, codigo_item, descripcion]):
            return False
        if self._is_non_item_text(descripcion):
            return False
        if not self._CAUSA_RE.match((causa_especifica or "").strip()):
            return False
        return True

    def _is_non_item_text(
        self,
        descripcion: str
    ) -> bool:

        if not descripcion:
            return False

        excluded = {
            "TOTAL",
            "TOTAL GLOSA",
            "TOTAL GLOSAS",
            "TOTAL FACTURADO",
            "TOTAL COBRADO",
            "OBSERVACIONES",
            "OBSERVACIONES GENERALES",
        }

        return descripcion.strip() in excluded
    