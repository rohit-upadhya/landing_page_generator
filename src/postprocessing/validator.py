from src.util.data_types import ErrorTypes

from lxml import html
import difflib


class Validator:
    def __init__(
        self,
        response_dict: dict,
        error_list: list = [],
    ):
        self.response_dict = response_dict
        self.error_list = error_list

    def validate(
        self,
    ):
        if "headline" not in self.response_dict.keys():
            self._log_errors(
                error_type=ErrorTypes.KEY_MISSING_ERROR, message="headline"
            )
        else:
            self._validate_headline(raw=self.response_dict.get("headline", ""))

        if "subheadline" not in self.response_dict.keys():
            self._log_errors(
                error_type=ErrorTypes.KEY_MISSING_ERROR, message="subheadline"
            )
        else:
            self._validate_subheadline(raw=self.response_dict.get("subheadline", ""))
        return self.error_list

    def _validate_headline(
        self,
        raw: str,
    ):
        tree = html.fromstring(raw)
        clean = html.tostring(tree, encoding="unicode")
        diff = list(difflib.unified_diff(raw.splitlines(), clean.splitlines()))
        if diff:
            self._log_errors(
                error_type=ErrorTypes.HTML_HEADLINE_PARSING_ERROR,
            )

    def _validate_subheadline(
        self,
        raw: str,
    ):
        tree = html.fromstring(raw)
        clean = html.tostring(tree, encoding="unicode")
        diff = list(difflib.unified_diff(raw.splitlines(), clean.splitlines()))
        if diff:
            self._log_errors(
                error_type=ErrorTypes.HTML_SUBHEADLINE_PARSING_ERROR,
            )

    def _log_errors(
        self,
        error_type: ErrorTypes,
        message: str = "",
        detail: str = "",
    ):
        self.error_list.append(
            {
                "error_type": error_type.value,
                "message": message,
                "detail": detail,
            }
        )
