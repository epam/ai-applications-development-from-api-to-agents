import logging

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.predefined_recognizers import CreditCardRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

logger = logging.getLogger(__name__)

_REDACTED = "***"
_NLP_CONFIG = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}


class _UMSCreditCardRecognizer(CreditCardRecognizer):
    """
    Extends Presidio's built-in CreditCardRecognizer to bypass Luhn validation.

    UMS generates fake/test card numbers that fail the Luhn checksum. The parent's
    validate_result() would silently drop every match by setting score → 0.0.
    This subclass overrides validate_result() to return None (= keep pattern score)
    and supplies UMS-specific patterns while inheriting context words and language
    support from the parent.

    Patterns cover all three credit card fields:
      - num:      Python dict / JSON dict / standalone
      - cvv:      Python dict / JSON dict
      - exp_date: Python dict / JSON dict
    """

    CONTEXT = CreditCardRecognizer.CONTEXT  # inherit parent context words

    def validate_result(self, pattern_text: str) -> None:
        """
        Skip Luhn checksum validation entirely.

        The parent's validate_result() runs a Luhn check and sets score → 0.0
        on failure.  UMS generates fake card numbers that never pass Luhn, so
        we return None here to preserve the original pattern score unchanged.
        """
        return None

    def __init__(self):
        ums_patterns = [
            # Card number inside Python dict:  'num': '5047-7145-8294-8166'
            Pattern(
                name="card_num_pydict",
                regex=r"(?<='num': ')\d{4}[-\s]\d{4}[-\s]\d{4}[-\s]\d{4}(?=')",
                score=0.95,
            ),
            # Card number inside JSON dict:  "num": "5047-7145-8294-8166"
            Pattern(
                name="card_num_json",
                regex=r'(?<="num": ")\d{4}[-\s]\d{4}[-\s]\d{4}[-\s]\d{4}(?=")',
                score=0.95,
            ),
            # Standalone card number (dashes or spaces) anywhere in text
            Pattern(
                name="card_num_standalone",
                regex=r"\b\d{4}[-\s]\d{4}[-\s]\d{4}[-\s]\d{4}\b",
                score=0.85,
            ),
            # CVV inside Python dict:  'cvv': '259'
            Pattern(
                name="card_cvv_pydict",
                regex=r"(?<='cvv': ')\d{3,4}(?=')",
                score=0.95,
            ),
            # CVV inside JSON dict:  "cvv": "259"
            Pattern(
                name="card_cvv_json",
                regex=r'(?<="cvv": ")\d{3,4}(?=")',
                score=0.95,
            ),
            # Expiry date inside Python dict:  'exp_date': '08/2029'
            Pattern(
                name="card_exp_pydict",
                regex=r"(?<='exp_date': ')\d{2}/\d{4}(?=')",
                score=0.95,
            ),
            # Expiry date inside JSON dict:  "exp_date": "08/2029"
            Pattern(
                name="card_exp_json",
                regex=r'(?<="exp_date": ")\d{2}/\d{4}(?=")',
                score=0.95,
            ),
        ]
        # Pass patterns to parent — this replaces the Luhn-based default patterns.
        super().__init__(patterns=ums_patterns)


class _UMSSalaryRecognizer(PatternRecognizer):
    """
    Detects salary values in YAML-like, JSON, Python-dict, and plain-text formats.

    Presidio has no built-in SALARY entity, and spaCy's MONEY NER label is too
    unreliable for structured key-value text without a currency symbol.
    A PatternRecognizer with lookbehind anchors is the correct approach here.

    Matches:
      - YAML:       salary: 85000
      - JSON:       "salary": 85000
      - Python dict:'salary': 85000
      - Plain text: Annual salary: $85,000   (case-insensitive)

    'salary: None' is safe — \\d requires at least one digit so None is skipped.
    """

    def __init__(self):
        super().__init__(
            supported_entity="SALARY",
            patterns=[
                Pattern(
                    name="salary_yaml",
                    regex=r"(?<=salary: )\d[\d,]*(?:\.\d+)?",
                    score=0.9,
                ),
                Pattern(
                    name="salary_json",
                    regex=r'(?<="salary": )\d[\d,]*(?:\.\d+)?',
                    score=0.9,
                ),
                Pattern(
                    name="salary_pydict",
                    regex=r"(?<='salary': )\d[\d,]*(?:\.\d+)?",
                    score=0.9,
                ),
                Pattern(
                    name="salary_text_currency",
                    regex=r"(?i)(?<=salary: )\$?[\d,]+(?:\.\d+)?",
                    score=0.85,
                ),
            ],
        )


class UMSDataGuardrail:
    """
    Redacts credit card numbers (num, cvv) and salary values from UMS tool results.

    Uses Presidio's analyze → anonymize pipeline with two dedicated recognizers:
      - UMSCreditCardRecognizer: extends built-in CreditCardRecognizer, bypasses Luhn
      - UMSSalaryRecognizer:     custom PatternRecognizer (no built-in SALARY entity)

    UMS returns data in a YAML-like format, e.g.:
        salary: 85000
        credit_card: {'num': '5047-7145-8294-8166', 'cvv': '259', 'exp_date': '10/2031'}
    """

    _ENTITIES = ["CREDIT_CARD", "SALARY"]
    _OPERATORS = {
        "CREDIT_CARD": OperatorConfig("replace", {"new_value": _REDACTED}),
        "SALARY": OperatorConfig("replace", {"new_value": _REDACTED}),
    }

    def __init__(self):
        self.analyzer = self._build_analyzer()
        self.anonymizer = AnonymizerEngine()
        logger.info("UMSDataGuardrail initialized")

    @staticmethod
    def _build_analyzer() -> AnalyzerEngine:
        #TODO:
        # - Create NlpEngineProvider with _NLP_CONFIG, build AnalyzerEngine from it
        # - Register _UMSCreditCardRecognizer and _UMSSalaryRecognizer
        # - Return analyzer
        raise NotImplementedError()

    def redact(self, text: str) -> str:
        """Redact credit card and salary data via Presidio analyze → anonymize pipeline."""
        #TODO:
        # - Analyze text for _ENTITIES; return text unchanged if no results
        # - Anonymize with _OPERATORS, return anonymized.text
        raise NotImplementedError()