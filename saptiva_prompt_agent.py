import os
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class SaptivaPromptAgent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": ("STRING", {"default": "gpt-4o"}),
                "prompt": ("STRING", {"forceInput": True}),
                "max_tokens": ("INT", {"default": 300, "min":1, "max":2048}),
                "temperature": ("FLOAT", {"default": 1.0, "min":0.0, "max":2.0}),
                "seed": ("INT", {"default": 42, "min":0, "max":999999}),  # New seed parameter
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "custom_prompt": ("STRING", {"default": "", "multiline": True}),
                "top_p": ("FLOAT", {"default":1.0, "min":0.0, "max":1.0}),
                "presence_penalty": ("FLOAT", {"default":0.0, "min":-2.0, "max":2.0}),
                "frequency_penalty": ("FLOAT", {"default":0.0, "min":-2.0, "max":2.0}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("processed_prompt", "generated_text")
    CATEGORY = "Saptiva Nodes"
    FUNCTION = "generate_text"

    def generate_text(self, model_name, prompt, max_tokens, temperature,
                      seed,
                      system_prompt="", custom_prompt="",
                      top_p=1.0, presence_penalty=0.0, frequency_penalty=0.0):

        if OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY not found in the .env file.")

        client = OpenAI(api_key=OPENAI_API_KEY)

        # Set the random seed to ensure that changing the seed input will produce a different suffix
        random.seed(seed)

        # Combine system and custom prompts
        system_msg = system_prompt.strip()
        if custom_prompt.strip():
            system_msg = (system_msg + "\n" + custom_prompt.strip()).strip()

        # Introduce a seed-based suffix to the user prompt to encourage variation
        random_suffix = f" [seed:{random.randint(1, 999999)}]"
        augmented_prompt = prompt.strip() + random_suffix

        messages = []
        if system_msg:
            messages.append({"role": "system", "content": system_msg})
        messages.append({"role": "user", "content": augmented_prompt})

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
        )

        if not response.choices or not response.choices[0].message:
            raise ValueError("No content in response")

        generated_text = response.choices[0].message.content.strip()
        processed_prompt = (system_msg + "\n" + augmented_prompt).strip()

        return (processed_prompt, generated_text)
