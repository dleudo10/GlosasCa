# from django.http import HttpResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from ..services.excel_export_service import ExcelExportService


# class ExportarGlosasView(APIView):
#     service_class = ExcelExportService

#     def post(self, request):
#         facturas = request.data.get("facturas", [])

#         try:
#             archivo = self.service_class().generar_excel(facturas)
#         except ValueError as exc:
#             return Response(
#                 {"detail": str(exc)},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return self._crear_respuesta_excel(archivo)

#     @staticmethod
#     def _crear_respuesta_excel(archivo):
#         response = HttpResponse(
#             archivo,
#             content_type="application/vnd.ms-excel",
#         )

#         response["Content-Disposition"] = (
#             'attachment; filename="glosas_exportadas.xls"'
#         )
        
#         return response

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.excel_export_service import (
    ExcelExportService,
    ItemsPendientesResolucionError,
)


class ValidarExportacionGlosasView(APIView):

    service_class = ExcelExportService

    def post(self, request):

        facturas = request.data.get(
            "facturas",
            []
        )

        resoluciones_items = request.data.get(
            "resoluciones_items",
            {}
        )

        try:

            pendientes = self.service_class().validar_exportacion(
                facturas=facturas,
                resoluciones_items=resoluciones_items,
            )

        except ValueError as exc:

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                    "errors": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "requiere_resolucion": bool(
                    pendientes
                ),
                "pendientes": pendientes,
            },
            status=status.HTTP_200_OK,
        )


class ExportarGlosasView(APIView):

    service_class = ExcelExportService

    def post(self, request):

        facturas = request.data.get(
            "facturas",
            []
        )

        resoluciones_items = request.data.get(
            "resoluciones_items",
            {}
        )

        try:

            archivo = self.service_class().generar_excel(
                facturas=facturas,
                resoluciones_items=resoluciones_items,
            )

        except ItemsPendientesResolucionError as exc:

            return Response(
                {
                    "success": False,
                    "requiere_resolucion": True,
                    "pendientes": exc.pendientes,
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        except ValueError as exc:

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                    "errors": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self._crear_respuesta_excel(
            archivo
        )

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