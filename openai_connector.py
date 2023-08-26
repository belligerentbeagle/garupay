import os
import openai

openai.api_key = "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"
messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},

]


messages.append({})
chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
reply = chat.choices[0].message.content


while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})