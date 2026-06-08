
import json, os
from groq import Groq
from ddgs import DDGS


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") or ""
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Tool implementation
def web_search(query: str):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    return [
        {
            "title": r["title"],
            "url": r["href"],
            "snippet": r["body"]
        }
        for r in results
    ]

def calculator(num1: float, num2: float):
    """Multiply two numbers"""
    result = num1 * num2
    return {
        "operation": "multiplication",
        "num1": num1,
        "num2": num2,
        "result": result
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First number to multiply"
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second number to multiply"
                    }
                },
                "required": ["num1", "num2"]
            }
        }
    }
]

# messages = [
#     {   "role": "system", 
#         "content": "You are a helpful assistant. Always use the Tools whenever necessary." 
#     },
#     {
#         "role": "user",
#         "content": "What is the result of 134534423404*-342343243242?"
#     }
# ]
messages = [
    {   "role": "system", 
        "content": "You are a helpful assistant. Always use the Tools whenever necessary." 
    },
    {
        "role": "user",
        "content": "Who is Captain of Indian Cricket Team?"
    }
]
GROQ_MODEL = "openai/gpt-oss-20b"
# First call: model decides whether to use tool
response = client.chat.completions.create(
    model=GROQ_MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

assistant_message = response.choices[0].message

# Add assistant message to history
messages.append(
    {
        "role": "assistant",
        "content": assistant_message.content,
        "tool_calls": assistant_message.tool_calls
    }
)

# Execute tools if requested
if assistant_message.tool_calls:

    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "web_search":
            result = web_search(arguments["query"])
        elif function_name == "calculator":
            result = calculator(arguments["num1"], arguments["num2"])

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        )
    messages.append({
        "role": "user",
        "content": "I have performed the tool usage. Here are the results. Summarize the results without anymore tool calls"
    })

    # Second call: model uses tool result
    final_response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages
    )
    print("*" * 50)
    print("Assistant:\n", final_response.choices[0].message.content)
    print("*" * 50)

else:
    print(assistant_message.content)