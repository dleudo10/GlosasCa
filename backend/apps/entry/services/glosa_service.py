from ..extractor.header_extractor import HeaderExtractor
from ..extractor.item_extractor import ItemExtractor
from ..services.pdf_read import PDFReader
from .item_enrichment_service import ItemEnrichmentService

class GlosaService:
    """
    Servicio principal para procesar una glosa.

    Orquesta:
    - lectura del PDF
    - extracción del encabezado
    - extracción de items

    En esta etapa NO consulta la base de datos.
    """

    def __init__(
        self,
        pdf_reader=None,
        header_extractor=None,
        item_extractor=None,
        enrichment_service=None,
    ):

        self.pdf_reader = pdf_reader or PDFReader()
        self.header_extractor = header_extractor or HeaderExtractor()
        self.item_extractor = item_extractor or ItemExtractor()
        self.enrichment_service = enrichment_service or ItemEnrichmentService()

    def process(self, file) -> dict:
        document = self.pdf_reader.read(file)
        encabezado = self.header_extractor.extract(document)
        print(encabezado)
        items = self.item_extractor.extract(document)
        
        items = self.enrichment_service.enrich_all(
            items=items,
            numero_factura=encabezado.get("numero_factura", ""),
            tipo_factura=encabezado.get("tipo_factura", "2"),
        )

        return {"encabezado": encabezado, "items": items}