import requests
import heapq
import os
import time
from dotenv import load_dotenv

from openai import OpenAI

import utils
from constants import Constants

load_dotenv()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_distance",
            "description": "Submit a word guess to the Clueless game API",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The next word guess"
                    }
                },
                "required": ["word"]
            }
        }
    }
]


def load_system_prompt(path="system_prompt.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def llm_call(min_heap):
    client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN"),
        )
    

    system_prompt = load_system_prompt()

    messages = [
            {"role": "system", "content": system_prompt},
        ]
    
    sorted_guesses = sorted(min_heap)   # sorts by distance automatically

    context_text = ""

    for distance, word in sorted_guesses[:20]:
        context_text += f"{word} — distance: {distance}\n"

    print(context_text)
    
    messages.append({
        "role": "user",
        "content": f"{context_text} \n\n\nGive your next word guess."
    })

    response = client.chat.completions.create(
            model=Constants.LLM_MODELS.value.get("kimi_k2_instruct"),
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=False,
            temperature=0.6,
            max_tokens=256
        )
    print(f"LLM response - {response}")
    return response.choices[0].message.content

def get_distance(word) -> dict:
    retry = True
    payload = {
        "categoryId": 0,
        "word": word,
        "challengeDate": utils.get_date()
    }

    while retry:
        print("hitting clueless api")
        response = requests.post(url=Constants.GUESS_URL.value, json=payload)
        if response.status_code == 500:
            print(f"Got a error code - {response.status_code}")
            time.sleep(1)
            continue
        return response.json()


def parse_api_response(response, min_heap) -> bool:

    if response.get("code") == "WORD_NOT_FOUND":
        return False
    
    if response["correct"]:
        return True
    
    heapq.heappush(min_heap, (response["distance"], response["word"]))
    return False

    


def main():
    min_heap = []
    # heapq.heappush(min_heap, (406, "pond"))

    for i in range(50):
        print(f"Guess number - {i + 1}")
        # Ask LLM to guess
        word = llm_call(min_heap)
        print(word)
        # word = "dummy"

        # Use the word that the LLM suggested and check the distance
        response = get_distance(word.lower())
        if parse_api_response(response, min_heap):
            return f"Won the game!!! - {word} is the answer!!"
        

if __name__ == '__main__':
    main()
