import base64
import os
import json

from datetime import datetime
from copy import deepcopy

from src.util.file_loader import FileLoader
from src.util.prompt_builder import Prompter
from src.inference.inference import Inference
from src.postprocessing.post_processor import PostProcessor


class PLP:
    def __init__(
        self,
        inputs: dict,
        prompt_template_file: str = "resources/prompt_template.yaml",
        num_retries: int = 3,
    ):
        self.file_loader = FileLoader()
        self.inputs = inputs
        self.num_retries = num_retries
        self.prompt_template = self._load_inputs(prompt_template_file)

    def _load_inputs(
        self,
        prompt_template_file: str,
    ):
        prompt_template = self.file_loader.load_file(prompt_template_file)
        return prompt_template

    def _infer(
        self,
        input_prompt: list[dict],
    ):
        inference_obj = Inference(input_prompt=input_prompt)
        return inference_obj.inference()

    def _load_prompter(
        self,
        prompt_template: dict,
        original_headline_html: str,
        original_subheadline_html: str,
        marketing_insights_text: str,
        image_in_base_64: str,
    ):
        return Prompter(
            prompt_template=prompt_template,
            original_headline_html=original_headline_html,
            original_subheadline_html=original_subheadline_html,
            marketing_insights_text=marketing_insights_text,
            image=image_in_base_64,
        )

    def _load_image(
        self,
        image_path: str,
    ):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            print(f"Issue loading image - {e}. Contact admin.")
            raise

    def _post_processor(
        self,
        response: str,
    ):
        post_processor = PostProcessor(response=response)
        error_list, parsable, response_output = post_processor.post_process()
        return error_list, parsable, response_output

    def plp_main(
        self,
    ):
        original_headline_html = self.inputs.get("original_headline_html", "")
        original_subheadline_html = self.inputs.get("original_subheadline_html", "")
        marketing_insights_text = self.inputs.get("marketing_insights_text", "")
        image_path = self.inputs.get("image_path", "")
        image_in_base_64 = self._load_image(image_path=image_path)
        prompt_builder = self._load_prompter(
            prompt_template=self.prompt_template,
            original_headline_html=original_headline_html,
            original_subheadline_html=original_subheadline_html,
            marketing_insights_text=marketing_insights_text,
            image_in_base_64=image_in_base_64,
        )
        prompt = prompt_builder.build_chat_prompt()
        response = self._infer(input_prompt=prompt)
        error_list, parsable, response_output = self._post_processor(response=response)

        result_dict = {
            "input": self.inputs,
            "error_list": [error_list],
            "last_parsable_result": {},
            "model_responses": [response],
        }
        if parsable:
            result_dict["last_parsable_result"] = response_output
        retry_num = 1
        while len(error_list) > 0 and retry_num <= self.num_retries:
            prompts = prompt_builder.reprompter(
                current_prompt=prompt, error_list=deepcopy(error_list)
            )
            del error_list
            response = self._infer(input_prompt=prompts)
            error_list, parsable, response_output = self._post_processor(
                response=response
            )
            result_dict["model_responses"].append(response)
            if parsable:
                result_dict["last_parsable_result"] = response_output
            result_dict["error_list"].append(error_list)
            retry_num += 1
        result_dict["final_result"] = result_dict["last_parsable_result"]

        self._logging_results(res_dict=result_dict)
        return result_dict

    def _logging_results(
        self,
        res_dict: dict,
        dir_path: str = "logs",
    ):
        os.makedirs(dir_path, exist_ok=True)
        filename = datetime.now().strftime("results_%Y%m%d_%H%M%S.json")
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(res_dict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    inputs = {
        "original_headline_html": """<h1 class="font-extrabold text-4xl lg:text-6xl tracking-tight md:-mb-4 flex flex-c
<span class="relative">Crush Your Personal Best with Nike Vaporfly 3 </span>
<span class="whitespace-nowrap relative ">
<span class="mr-3 sm:mr-4 md:mr-5">Engineered for </span>
<span class=" relative whitespace-nowrap">
<span class="absolute bg-neutral-content -left-2 -top-1 -bottom-1 -right-2 md:-l
<span class="relative text-neutral">Race-Day Speed</span>
</span>
</span>
</h1>""",
        "original_subheadline_html": """<p class="text-lg opacity-80 leading-relaxed">Maximize your race-day poten
tial with cutting-edge energy return, lightweight durability, and a sleek, aerody
namic design that keeps you ahead of the competition.</p>""",
        "marketing_insights_text": """Product Name:
Nike Vaporfly 3 Men's Road Racing Shoes
Product Description:
The Nike Vaporfly 3 is a high-performance road racing shoe designed to give run
Unique Selling Proposition (USP):
Features and Benefits:
Race-Day Optimized Performance
Feature: Specifically engineered for race-day speed and agility.
Benefit: Gives runners the competitive edge to push their limits in both short and
Lightweight Yet Durable Design
Feature: Lightweight structure with reinforced durability.
Benefit: Ensures long-lasting comfort and durability without compromising perfor
Advanced Energy Return System
Feature: Innovative sole for maximum energy return.
Benefit: Helps runners conserve energy, reduce fatigue, and maintain speed thro
Versatile for All Levels
Feature: Suitable for elite racers and casual runners.
Benefit: Allows beginners to boost performance while offering the necessary sup
Innovative Colorways
Feature: Available in multiple stylish color combinations.
Benefit: Provides a combination of style and speed, letting runners look and feel
Target Audience:
Potential Audiences:
Elite and Competitive Runners
Desires: To break personal records and optimize their race-day performance.
Painpoints: Difficulty finding shoes that maximize speed without compromising c
Fears: Fear of shoes wearing out or failing during key races; not reaching full pot
Aspirations: To push their athletic limits and compete at the highest level.
Amateur Runners Preparing for Races
Desires: To improve performance, especially for significant races like 10Ks or ma
Painpoints: The challenge of finding a shoe that balances comfort, durability, and
Fears: Not having the right equipment to achieve their best results.
Aspirations: To perform well in their first competitive races and gradually improve
Fitness Enthusiasts Who Train Regularly
Desires: To benefit from advanced technology in their footwear, enhancing daily
Painpoints: Inconsistent energy return or shoes that cause fatigue over long dista
Fears: Wearing shoes that don't support their training routine or exacerbate injury
Aspirations: To elevate their training sessions with high-performance gear.
Style-Conscious Athletes
Desires: To look as good as they perform, combining fashion with functionality.
Painpoints: Limited selection of stylish running shoes that also meet high-perform
Fears: That high-performance shoes compromise on style or vice versa.
Aspirations: To stand out on the track with footwear that delivers on both perform
Unaware Stage:
Psychological Trigger: Curiosity about the link between footwear and improved p
Marketing Angle: Educate through engaging content about the role advanced sho
Problem Aware Stage:
Psychological Trigger: Frustration with existing shoes not delivering expected res
Marketing Angle: Use testimonials and comparisons that highlight how Vaporfly 3
Solution Aware Stage:
Psychological Trigger: Desire for certainty that the Vaporfly 3 will elevate their pe
Marketing Angle: Emphasize product specs, energy return technology, and durab""",
        "image_path": "resources/test.png",
    }

    plp = PLP(
        inputs=inputs,
    )
    print(plp.plp_main())
    pass
