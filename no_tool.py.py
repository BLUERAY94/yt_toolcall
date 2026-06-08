
import os
from groq import Groq

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") or ""
GROQ_MODEL = "llama-3.3-70b-versatile"
client     = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [
    {
        "role": "user",
        "content": "What is the result of 134534423404*-342343243242?"
    }
]
# messages = [
#     {
#         "role": "user",
#         "content": "Who is Captain of Indian Cricket Team?"
#     }
# ]

response          = client.chat.completions.create(messages=messages,model=GROQ_MODEL)
assistant_message = response.choices[0].message
print("*" * 50)
print("Assistant:\n", assistant_message.content)
print("*" * 50)