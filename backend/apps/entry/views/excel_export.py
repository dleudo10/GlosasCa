from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.excel_export_service import ExcelExportService


class ExportarGlosasView(APIView):
    service_class = ExcelExportService

    def post(self, request):
        facturas = request.data.get("facturas", [])

        try:
            archivo = self.service_class().generar_excel(facturas)
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self._crear_respuesta_excel(archivo)

    # @staticmethod
    # def _crear_respuesta_excel(archivo):
    #     response = HttpResponse(
    #         archivo,
    #         content_type=(
    #             "application/vnd.openxmlformats-officedocument."
    #             "spreadsheetml.sheet"
    #         ),
    #     )

    #     response["Content-Disposition"] = (
    #         'attachment; filename="glosas_exportadas.xlsx"'
    #     )

    #     return response
    
    @staticmethod
    def _crear_respuesta_excel(archivo):
        response = HttpResponse(
            archivo,
            content_type="application/vnd.ms-excel",
        )

        response["Content-Disposition"] = (
            'attachment; filename="glosas_exportadas.xls"'
        )
        
        return response

