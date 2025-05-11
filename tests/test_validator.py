import pytest
from src.postprocessing.validator import Validator
from src.util.data_types import ErrorTypes


@pytest.mark.parametrize(
    "payload,expected",
    [
        # ({"headline": "<h1>good</h1>", "subheadline": "<p>good</p>"}, []),
        (
            {"headline": "<h1>bad", "subheadline": "<p>good</p>"},
            [ErrorTypes.HTML_HEADLINE_PARSING_ERROR.value],
        ),
        ({"subheadline": "<p>good</p>"}, [ErrorTypes.KEY_MISSING_ERROR.value]),
    ],
)
def test_validate(payload, expected):
    v = Validator(payload)
    errors = [e["error_type"] for e in v.validate()]
    print(errors, expected)
    assert sorted(errors) == sorted(expected)
