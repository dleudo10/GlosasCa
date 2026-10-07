from django.urls import path
from .views import (
    PuntosRutaView,
    PDFUploadView,
    FacturaItemsView,
    ExportarGlosasView,
    ValidarExportacionGlosasView,
)

urlpatterns = [
    path("upload/", PDFUploadView.as_view(), name="pdf-upload"),
    path("factura/<str:numero_factura>/items/", FacturaItemsView.as_view(), name="factura-items"),
    path("puntos-ruta/", PuntosRutaView.as_view(), name="glosas-puntos-ruta"),
    path("exportar/", ExportarGlosasView.as_view(), name="exportar-glosas"),
    path("exportar/validar/", ValidarExportacionGlosasView.as_view(), name="validar-exportacion-glosas", ),
]