from enum import Enum


class ErrorTypes(Enum):
    JSON_PARSING_ERROR = "json_parsing_error"
    HTML_HEADLINE_PARSING_ERROR = "html_headline_parsing_error"
    HTML_SUBHEADLINE_PARSING_ERROR = "html_subheadline_parsing_error"
    KEY_MISSING_ERROR = "key_missing_error"


class ModelType(Enum):
    OPEN_AI = "open_ai"
