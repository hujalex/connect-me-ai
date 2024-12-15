import pandas as pd
import os
from groq import Groq
import json
import sys
from dotenv import load_dotenv

load_dotenv()

#Open data
with open('./data/handbook.json', 'r') as file:
    handbook_data = json.load(file)
with open('./data/tutorresources.json', 'r') as file:
    tutor_resources_data = json.load(file);

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

for line in sys.stdin:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"{handbook_data} {tutor_resources_data} Your are a helpful assistant answering questions based off the data given",
            },
            {
                "role": "system",
                "content": f"Provide links as much as possible",
            },
            {
                "role":"system",
                "content" : "Always provide the CONNECT_ME_HANDBOOK link if necessary to question"
            },
            {
                "role": "user",
                "content": f"{line}",
            },
        ],
        model="llama3-70b-8192",
    )

    print(chat_completion.choices[0].message.content)

