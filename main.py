import openai
import discord
from discord import Client
import json

INIT_PARAMETER = json.load(open("config.json", "r"))

INIT_PREFIX = INIT_PARAMETER["INIT_PREFIX"]
MEMORY_THRESHOLD = INIT_PARAMETER["INIT_THRESHOLD"]


class AI:
    def __init__(self, key:str) -> None:
        """
        initialize the function with prefix in the config file.
        
        prefix  -> used in the openai's api prompt
        history -> to give this bot some sort of memory

        Args:
            key (string): openai's api key
        """
        self.prefix = INIT_PREFIX
        self.memory_threshold = MEMORY_THRESHOLD
        self.history = ""
        openai.api_key = key

    def __update_prompt(self, question:str, answer:str):
        """
        update the chat history and rotate the history if question count exceed certain threshold

        Args:
            question (string): the question you ask the bot
            answer (string): the answer replied by openai's api
        """
        if self.history.count("Q:") > self.memory_threshold:
            self.history = self.history[self.history[2:].index("Q") + 1 :]
        self.history += f"\nQ:{question}\nA:{answer}\n"

    def generate_response(self, question: str):
        """
        call the openai's api to generate response to the question you ask 

        Args:
            question (string): the question you ask

        Returns:
            answer (string): answer responed by openai's api 
        """
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{self.prefix}{self.history}Q:{question}\nA:",
            temperature=0.9,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        answer = response["choices"][0]["text"].strip(" \n")
        self.__update_prompt(question, answer)
        return answer

    def get_history(self, content=None):
        """
        return the chat history in this form:
            Q: the question you ask
            A: tae answer api give

        Returns:
            history: the chat history with openai's bot
        """
        return self.history

    def update_prefix(self, content:str):
        """
        update the prompt of the bot

        Args:
            content (string): the prompt text you want to use

        Returns:
            info: notify the changed prompt
        """ 
        self.prefix = content
        return f"prefix changed to: {self.prefix}"

    def clear_history(self, content=None):
        """
        clear the chat history with the bot

        Returns:
            info: notify the history is cleared
        """
        self.history = ""
        return "chat history cleared"

    def reset_prefix(self, content=None):
        """
        reset the prompt to the default in config.json

        Returns:
            info: notify the prompt text is reset
        """
        self.prefix = INIT_PREFIX
        self.clear_history()
        return "prefix reset"


class discord_bot(Client):
    def __init__(self, keys):
        """
        initialize the code with give api keys

        Args:
            keys (dictionary): dictionary of api keys or token
        """
        super().__init__()
        self.TOKEN = (keys["discord"])
        self.bt = AI(keys["openai"])

        self.function = {
            "history": self.bt.get_history,
            "update": self.bt.update_prefix,
            "clear": self.bt.clear_history,
            "reset": self.bt.reset_prefix,
        }

    @Client().event
    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game("The Anglo-Saxon Mission"),
        )

    @Client().event
    async def on_message(self, message):
        if message.author == self.user:
            return
        else:
            try:
                msg = self.message_handler(message.content)
                await message.channel.send(msg)
            except:
                return

    def message_handler(self, content):
        if content.startswith("/ai"):
            content = content.strip("/ai ")
            msg = self.function.get(content.split()[0], self.bt.generate_response)(
                content.split()[-1]
            )
            return msg
        else:
            return

    def run(self):
        super().run(self.TOKEN)


if __name__ == "__main__":
    keys = json.load(open("./keys.json", "r"))
    db = discord_bot(keys)
    db.run()
