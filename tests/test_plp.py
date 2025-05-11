import json
from src.plp import PLP


def _inputs(prompt_yaml, tiny_png):
    return {
        "original_headline_html": "<h1>old</h1>",
        "original_subheadline_html": "<p>old</p>",
        "marketing_insights_text": "MI",
        "image_path": tiny_png,
    }


def test_plp_success(
    fake_openai,
    prompt_yaml,
    tiny_png,
    tmp_path,
    monkeypatch,
):
    # ensure prompts load from tmp YAML
    monkeypatch.setattr(
        "src.plp.PLP._load_inputs",
        lambda self, _: {
            "system_prompt": "sys",
            "user_prompt": "{ORIGINAL_HEADLINE_HTML}",
            "reprompts": {"intial_message": "fix"},
            "final_message": "end",
        },
    )
    plp = PLP(inputs=_inputs(prompt_yaml, tiny_png))
    res = plp.plp_main()
    assert res["error_list"][0] == []
    assert "headline" in res["final_result"]


def test_plp_retry_on_bad_json(monkeypatch, prompt_yaml, tiny_png):
    calls = iter(
        [
            '{"wrong":}',
            json.dumps({"headline": "<h1>X</h1>", "subheadline": "<p>Y</p>"}),
        ]
    )

    class _Fake:
        def generate_response(self, message):
            return next(calls)

    monkeypatch.setattr("src.inference.inference.OpenAICaller", _Fake)
    plp = PLP(inputs=_inputs(prompt_yaml, tiny_png), num_retries=1)
    res = plp.plp_main()
    assert len(res["error_list"][0]) > 0
    assert res["error_list"][-1] == []
    assert res["final_result"]["headline"] == "<h1>X</h1>"
