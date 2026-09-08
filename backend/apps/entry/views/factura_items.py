from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..repositories.his_repository import HISRepository


class FacturaItemsView(APIView):
    """
    Devuelve los ítems del HIS para una factura, excluyendo los códigos
    ya detallados en el PDF. Alimenta el modal donde la analista
    selecciona los ítems que completan el valor de los ítems globales.
    """

    def post(self, request, numero_factura):

        tipo_factura = request.query_params.get("tipo", "2")
        codigos_excluir = request.data.get("codigos_excluir", [])

        if not isinstance(codigos_excluir, list):
            return Response(
                {
                    "success": False,
                    "error": "codigos_excluir debe ser una lista.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            items = HISRepository().obtener_items_factura(
                numero_factura=numero_factura,
                tipo_factura=tipo_factura,
                codigos_excluir=codigos_excluir,
            )
        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "error": "Ocurrió un error consultando el HIS.",
                    "detail": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "success": True,
                "numero_factura": numero_factura,
                "tipo_factura": tipo_factura,
                "total": len(items),
                "items": items,
            },
            status=status.HTTP_200_OK,
        )