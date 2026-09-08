class ConfidenceCalculator:

    def calculate(self, signals):

        score = 0
        max_score = 0

        strong_signals = 0

        for name, signal in signals.items():

            # Peso máximo
            from ..patterns.glosa_patterns import GLOSA_PATTERNS

            config = GLOSA_PATTERNS[name]

            weight = config["weight"]

            max_score += weight

            if signal["found"]:

                score += weight

                if signal["strong"]:
                    strong_signals += 1

        if max_score == 0:
            return {
                "score": 0,
                "confidence": 0,
                "strong_signals": 0,
            }

        confidence = score / max_score

        return {
            "score": score,
            "confidence": round(confidence, 2),
            "strong_signals": strong_signals,
        }