from typing import Optional


class Prompter:
    def __init__(
        self,
        prompt_template: dict[any, any],
        original_headline_html: Optional[str] = None,
        original_subheadline_html: Optional[str] = None,
        marketing_insights_text: Optional[str] = None,
        image: any = None,
    ):
        self.prompt_template = prompt_template
        self.original_headline_html = original_headline_html
        self.original_subheadline_html = original_subheadline_html
        self.marketing_insights_text = marketing_insights_text
        self.image = image
        if not self.prompt_template:
            raise ValueError(
                "Prompt template is not provided. Please provide a prompt template for further processing."
            )
        pass

    def build_chat_prompt(
        self,
    ) -> list[dict[str, str]]:
        final_prompt = []
        if "system_prompt" in self.prompt_template:
            content = self.prompt_template.get("system_prompt", "")
            final_prompt.append({"role": "system", "content": content})

        if (
            self.original_headline_html
            and self.original_subheadline_html
            and self.marketing_insights_text
        ):
            content = self.prompt_template.get("user_prompt", "").format(
                ORIGINAL_HEADLINE_HTML=self.original_headline_html,
                ORIGINAL_SUBHEADLINE_HTML=self.original_subheadline_html,
                MARKETING_INSIGHTS_TEXT=self.marketing_insights_text,
            )
            final_prompt.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": content,
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{self.image}",
                        },
                    ],
                }
            )
        else:
            raise ValueError("No text provided. Please provide a query and try again.")
        return final_prompt
