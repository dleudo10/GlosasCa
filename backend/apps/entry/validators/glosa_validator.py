from ..services.pdf_read import PDFReader
from .glosa_detector import GlosaDetector
from .confidence import ConfidenceCalculator

class GlosaValidator:

    def __init__(self):

        self.reader = PDFReader()

        self.detector = GlosaDetector()

        self.confidence = ConfidenceCalculator()

    def validate(self, file):

        pdf_content = self.reader.read(file)

        detection = self.detector.detect(
            pdf_content
        )

        confidence = self.confidence.calculate(
            detection["signals"]
        )

        status = self._determine_status(
            confidence
        )

        return {
            "is_glosa": status == "valid",

            "status": status,

            "score": confidence["score"],

            "confidence": confidence["confidence"],

            "strong_signals": confidence["strong_signals"],

            "signals": detection["signals"],

            "pages_analyzed": pdf_content["total_pages"],
        }

    def _determine_status(self, result):

        confidence = result["confidence"]

        strong_signals = result["strong_signals"]

        if confidence >= 0.60 and strong_signals >= 2:

            return "valid"

        if confidence >= 0.30 and strong_signals >= 1:

            return "review"

        return "invalid"