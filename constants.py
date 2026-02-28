from enum import Enum

class Constants(Enum):
    GUESS_URL = "https://api.lessgames.com/clueless/guess"

    LLM_MODELS = {
        "kimi_k2_instruct": "moonshotai/Kimi-K2-Instruct-0905",
        "qwen_3_5": "Qwen/Qwen3.5-397B-A17B:novita",
        "deepseek_r1": "deepseek-ai/DeepSeek-R1:novita"
    }

