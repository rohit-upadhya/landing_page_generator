import json

from util.data_types import ErrorTypes


class Parser:
    def __init__(
        self,
        response: str,
    ):
        self.error_list = []
        self.parsable = True
        self.response = response

    def parse(
        self,
    ):
        response_output = {}
        try:
            response_output = json.loads(self.response)
        except Exception as e:
            self._log_errors(error_type=ErrorTypes.JSON_PARSING_ERROR, message=f"{e}")
            self.parsable

        return response_output, self.error_list, self.parsable

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
