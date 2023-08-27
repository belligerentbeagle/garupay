import openai

openai.api_key = "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"
messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

MESSAGE_0 = "User : let me give you a situation, and you help to settle up who owes how much to the group. " \
            "let me give you an example first: there is a group of 2 people, A and B. A paid for a meal which was " \
            "shared equally with B. This meal cost $40. This means A paid $40, but only ate half of what it is " \
            "worth. B ate half the meal too but did not eat any money. So when settling up, A should owe -$20, " \
            "because he is owed $20 from the others. B should owe $20, because he owes $20 from the others. " \
            "I want the output to be ONLY a dictionary, without any explanation. " \
            "The output should be {'A': -20, 'B': 20}. The total sum in the " \
            "values in the dictionary should be 0. Do you understand this?"
messages.append({"role": "user", "content": MESSAGE_0})
chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
reply = chat.choices[0].message.content
print(reply)

MESSAGE_1 = "User : let me give you another situation. A owes me $5. So when settling up, A should owes $5, while I " \
            "owes -$5. The output should be {'A': 5, 'Me': -5}."
messages.append({"role": "user", "content": MESSAGE_1})
chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
reply = chat.choices[0].message.content
print(reply)

MESSAGE_1 = "User : I owe Gab $5. I owe Ruiheng $20. The output should be {'Gab': -5, 'Ruiheng': '-20', 'Me': 25}."
messages.append({"role": "user", "content": MESSAGE_1})
chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
reply = chat.choices[0].message.content
print(reply)


def query_openai(message):
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
    return reply
