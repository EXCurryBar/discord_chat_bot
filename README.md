## Discord chat bot

I just hook discord bot with openai's text-davinci-003 model. Nothing to see here.

---
The content in `keys.json` should be like this:
```json
{
    "discord": "YOUR DISCORD BOT'S TOKEN HERE",
    "openai" : "YOUR OPENAI API KEY HERE"
}
```

---

The content in `config.json` should be like this, for the prompt content's example, you can check [here](https://prompts.chat/):

```json
{
    "INIT_THRESHOLD" : 100, // how many question/answer pairs should the bot remember
    "INIT_PREFIX" : "prompt content"
}
```