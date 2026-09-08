from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from ..validators import PDFValidation
from ..validators.glosa_validator import GlosaValidator
from ..services.glosa_service import GlosaService


class PDFUploadView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):

        files = request.FILES.getlist("files")

        if not files:

            return Response(
                {
                    "success": False,
                    "error": "No se enviaron archivos.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        glosa_validator = GlosaValidator()

        glosa_service = GlosaService()

        results = []

        for file in files:

            # ==================================================
            # 1. Validación física del PDF
            # ==================================================

            pdf_validation = (
                PDFValidation.execute(file)
            )

            if not pdf_validation["valid"]:

                results.append({
                    "name": file.name,
                    "valid": False,
                    "error": pdf_validation["error"],
                })

                continue

            # ==================================================
            # 2. Validar que sea una glosa
            # ==================================================

            glosa_validation = (
                glosa_validator.validate(file)
            )

            if not glosa_validation["is_glosa"]:

                results.append({
                    "name": file.name,
                    "valid": False,
                    "error": (
                        "El documento no parece "
                        "ser una glosa."
                    ),
                    "validation": glosa_validation,
                })

                continue

            # ==================================================
            # 3. Procesar glosa
            # ==================================================

            try:

                data = glosa_service.process(
                    file
                )

                results.append({
                    "name": file.name,
                    "valid": True,
                    "encabezado": data["encabezado"],
                    "items": data["items"],
                    "total_items": len(
                        data["items"]
                    ),
                })

            except Exception as exc:

                results.append({
                    "name": file.name,
                    "valid": False,
                    "error": (
                        "Ocurrió un error procesando "
                        "el documento."
                    ),
                    "detail": str(exc),
                })

        return Response(
            {
                "success": True,
                "total": len(files),
                "glosas": results,
            },
            status=status.HTTP_200_OK,
        )
 