import discord
from AI import AI
import json

token = json.load(open("keys.json", 'r'))

intents = discord.Intents.default()
intents.message_content = True
client =  discord.Client(intents=intents)

ai = AI(token["openai"])

functions = {
    "clear" : ai.clear_history,
    "reset" : ai.reset_prefix,
    "update": ai.update_prefix,
    "history":ai.get_history
}


@client.event
async def on_ready():
    game = discord.Game("gpt 3.5-turbo")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
   
    if message.content.startswith("/ai"):
        msg = message.content.strip("/ai ")
        command = msg.split(' ')[0]
        try:
            response = functions[command](msg.strip(command))
        except:
            response = ai.generate_response(msg)
            
        await message.channel.send(response)

client.run(token["discord"])

