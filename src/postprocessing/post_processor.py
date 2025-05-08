from src.postprocessing.parser import Parser
from src.postprocessing.validator import Validator


class PostProcessor:
    def __init__(
        self,
        response: str,
    ):
        self.response = response
        self.error_list = []
        pass

    def post_process(
        self,
    ):
        parser = Parser(response=self.response)
        response_output, parse_error_list, parsable = parser.parse()
        self.error_list.extend(parse_error_list)
        if parsable:
            validator = Validator(response_dict=response_output)
            val_error_list = validator.validate()
            self.error_list.extend(val_error_list)
        return self.error_list, parsable, response_output
