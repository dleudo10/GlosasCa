from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..repositories.his_repository import HISRepository

class PuntosRutaView(APIView):
    """SELECT PUNRUTCOD FROM PUNRUT WHERE PUNRUTEST = 'A'"""

    def get(self, request):
        try:
            puntos = HISRepository().obtener_puntos_ruta()
        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "error": "Ocurrió un error consultando los puntos de ruta.",
                    "detail": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {"success": True, "total": len(puntos), "puntos": puntos},
            status=status.HTTP_200_OK,
        )