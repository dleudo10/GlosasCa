import re

from ..patterns.glosa_patterns import GLOSA_PATTERNS
from ..services.normalizer import TextNormalizer


class GlosaDetector:

    def detect(self, pdf_content):

        searchable_content = self._build_searchable_content(
            pdf_content
        )

        signals = {}

        for signal_name, config in GLOSA_PATTERNS.items():

            matches = []

            for pattern in config.get("patterns", []):

                found = re.findall(
                    pattern,
                    searchable_content,
                    re.IGNORECASE
                )

                if found:
                    matches.extend(found)

            keyword_matches = []

            for keyword in config.get("keywords", []):

                normalized_keyword = (
                    TextNormalizer.normalize_for_search(keyword)
                )

                if normalized_keyword in searchable_content:
                    keyword_matches.append(keyword)

            total_matches = len(set(matches + keyword_matches))

            signals[signal_name] = {
                "found": total_matches >= config.get(
                    "min_matches",
                    1
                ),
                "matches": total_matches,
                "strong": config.get("strong", False),
            }

        return {
            "signals": signals,
            "content": searchable_content,
        }

    def _build_searchable_content(self, pdf_content):

        chunks = []

        for page in pdf_content["pages"]:

            text = page.get("text", "")

            if text:
                chunks.append(
                    TextNormalizer.normalize_for_search(text)
                )

            for table in page.get("tables", []):

                for row in table:

                    row_text = " ".join(
                        str(cell or "")
                        for cell in row
                    )

                    if row_text:

                        chunks.append(
                            TextNormalizer.normalize_for_search(
                                row_text
                            )
                        )

        return "\n".join(chunks)