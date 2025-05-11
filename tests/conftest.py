import json, base64, pathlib, pytest
from datetime import datetime


@pytest.fixture
def good_response():
    return json.dumps(
        {"headline": '<h1 class="x">Head</h1>', "subheadline": '<p class="y">Sub</p>'}
    )


@pytest.fixture
def bad_json():
    return '{"headline": "<h1>" }'


@pytest.fixture
def fake_openai(monkeypatch, good_response):
    class _FakeCaller:
        def generate_response(self, message):
            return good_response

    monkeypatch.setattr(
        "src.inference.inference.OpenAICaller", _FakeCaller, raising=True
    )


@pytest.fixture
def prompt_yaml(tmp_path):
    content = {
        "system_prompt": "system here",
        "user_prompt": "{ORIGINAL_HEADLINE_HTML}",
        "reprompts": {"intial_message": "fix:"},
        "final_message": "end",
    }
    f = tmp_path / "prompt_template.yaml"
    f.write_text(json.dumps(content))
    return str(f)


@pytest.fixture
def tiny_png(tmp_path):
    png_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
        "ASsJTYQAAAAASUVORK5CYII="
    )
    file = tmp_path / "x.png"
    file.write_bytes(png_bytes)
    return str(file)
