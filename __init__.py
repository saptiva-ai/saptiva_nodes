from .saptiva_prompt_agent import SaptivaPromptAgent

NODE_CLASS_MAPPINGS = {
    "SaptivaPromptAgent": SaptivaPromptAgent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaptivaPromptAgent": "Saptiva Prompt Agent"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
