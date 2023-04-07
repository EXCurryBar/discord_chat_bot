import openai
import discord
from discord import Client
import json

INIT_PARAMETER = json.load(open("config.json", "r"))

INIT_PREFIX = INIT_PARAMETER["INIT_PREFIX"]
MEMORY_THRESHOLD = INIT_PARAMETER["INIT_THRESHOLD"]


class AI:
    def __init__(self, key: str) -> None:
        """
        initialize the function with prefix in the config file.

        prefix  -> used in the openai's api prompt
        history -> to give this bot some sort of memory

        Args:
            key (string): openai's api key
        """
        self.prefix = INIT_PREFIX
        self.memory_threshold = MEMORY_THRESHOLD
        self.memory_use = 0
        self.history = [
            {"role": "system", "content": self.prefix},
        ]
        openai.api_key = key


    def generate_response(self, question: str):
        try:
            self.history.append({"role": "user", "content": question})
            if len(self.history) > 16:
                self.history.pop(1)
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.history)
            self.memory_use+=response["usage"]["total_tokens"]
            res = response["choices"][0]["message"]
            self.history.append(res)
            return res["content"]
        except Exception as e:
            # Except encounter some api error
            return str(e)


    def get_history(self, content=None):
        output = str()
        for item in self.history:
            if item["role"] == "assistant":
                output+="A: "
            elif item["role"] == "user":
                output+="Q: "
            else:
                continue
            output+= item["content"]+"\n"

        return output
    
    
    def get_token(self, content=None):
        return str(self.memory_use)


    def update_prefix(self, content: str):
        self.history = [
            {"role": "system", "content": content},
        ]

        return f"prefix change to {self.history[0]['content']}"


    def clear_history(self, content=None):
        self.history = [self.history[0]]
        return "history cleared"


    def reset_prefix(self, content=None):
        self.history = [
            {"role": "system", "content": INIT_PREFIX},
        ]
        return "prefix reset to default"
