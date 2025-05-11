from src.util.prompt_builder import Prompter


def test_prompt_build(prompt_yaml, tiny_png):
    tpl = {"system_prompt": "sys", "user_prompt": "X"}
    p = Prompter(tpl, "H", "S", "M", image="Z")
    chat = p.build_chat_prompt()
    assert chat[0]["role"] == "system"
    assert chat[1]["content"][1]["type"] == "input_image"
