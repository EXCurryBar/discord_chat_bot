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
            if self.memory_use>=3000:
                self.history.pop(1)
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.history)
            self.memory_use+=response["usage"]["total_tokens"]
            self.history.append(res:=response["choices"][0]["message"])
            return res["content"]
        except Exception as e:
            # Except encounter some api error
            return str(e)


    def get_history(self, content=None):
        # TODO this
        pass
    
    
    def get_token(self, content=None):
        return str(self.memory_use)


    def update_prefix(self, content: str):
        self.history = [
            {"role": "system", "content": content},
        ]

        pass

    def clear_history(self, content=None):
        self.history = self.history[0]
        pass

    def reset_prefix(self, content=None):
        self.history = [
            {"role": "system", "content": INIT_PREFIX},
        ]
        pass
