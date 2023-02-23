from main import AI
import json

def main():
    bot = AI(json.load(open("./keys.json",'r'))["openai"])
    while True:
        q = input("chat: ")
        match (q.split(" ")[0]):
            case "update":
                bot.update_prefix(q.strip("update "))
            case "clear":
                bot.clear_history()
            case "history":
                bot.get_history()
            case "reset":
                bot.reset_prefix()
            case _:
                a = bot.generate_response(q)
                print(a)
        
main()