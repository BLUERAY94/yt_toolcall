# Understanding Tool Calling in LLMs

## Introduction

Large Language Models (LLMs) are excellent at generating text, reasoning, and answering questions. However, they have two important limitations:

1. **They may hallucinate facts** when asked about current information.
2. **They are not reliable calculators** for large numerical computations.

Tool Calling solves these problems by allowing an LLM to invoke external functions whenever additional capabilities are needed.

This repository demonstrates the difference between:

* **`no_tool.py`** → Pure LLM response
* **`tool_caller.py`** → LLM enhanced with tools

---

# Why Tool Calling Matters

Imagine asking an LLM:

> What is the result of 134534423404 × -342343243242?

A standalone LLM may attempt to compute the answer itself and produce an incorrect result.

Similarly, if you ask:

> Who is the current captain of the Indian Cricket Team?

The model may provide outdated information depending on its training data.

Tool Calling allows the model to:

* Use a calculator for arithmetic
* Search the web for current information
* Access databases and APIs
* Interact with external systems

This transforms an LLM from a text generator into an intelligent agent.

---

# Example 1: LLM Without Tools

File:

```bash
no_tool.py
```

## How It Works

The program:

1. Creates a Groq client
2. Sends a user message directly to the LLM
3. Prints the response

```python
response = client.chat.completions.create(
    messages=messages,
    model=GROQ_MODEL
)
```

The model must answer using only its internal knowledge and reasoning.

---

## Request Flow

```text
User Question
      |
      v
     LLM
      |
      v
Generated Response
```

No external systems are available.

---

## Limitations

### Mathematical Computation

For very large calculations:

```text
134534423404 * -342343243242
```

The model may:

* Estimate incorrectly
* Make arithmetic mistakes
* Produce inconsistent answers

### Current Information

Questions such as:

```text
Who is Captain of Indian Cricket Team?
```

may return outdated information because the model does not have real-time access to the web.

---

# Example 2: LLM With Tool Calling

File:

```bash
tool_caller.py
```

This example gives the LLM access to two tools:

1. Calculator
2. Web Search

---

# Tool 1: Calculator

```python
def calculator(num1, num2):
```

Purpose:

* Multiply two numbers
* Return structured results

Example output:

```json
{
  "operation": "multiplication",
  "num1": 5,
  "num2": 7,
  "result": 35
}
```

---

# Tool 2: Web Search

```python
def web_search(query):
```

Uses:

```python
DDGS()
```

to search the web and return results.

Example output:

```json
[
  {
    "title": "...",
    "url": "...",
    "snippet": "..."
  }
]
```

---

# Defining Tools for the Model

The model cannot call Python functions directly.

We must describe each tool using a schema.

Example:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            ...
        }
    }
]
```

This tells the model:

* Tool name
* Purpose
* Required parameters
* Expected argument types

---

# Step 1: User Sends Request

Example:

```python
{
    "role": "user",
    "content": "Who is Captain of Indian Cricket Team?"
}
```

---

# Step 2: Model Decides Whether a Tool Is Needed

The first LLM call includes:

```python
tool_choice="auto"
```

```python
response = client.chat.completions.create(
    model=GROQ_MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

At this stage, the model does not answer immediately.

Instead, it decides:

```text
Can I answer this myself?
or
Should I call a tool?
```

---

# Step 3: Tool Call Generation

For a current-events question, the model may generate:

```json
{
  "name": "web_search",
  "arguments": {
    "query": "current captain of Indian cricket team"
  }
}
```

No tool has run yet.

The model is simply requesting one.

---

# Step 4: Python Executes the Tool

Your code receives the request:

```python
if function_name == "web_search":
    result = web_search(...)
```

The actual Python function is executed.

---

## Flow

```text
User
 |
 v
LLM
 |
 |-----> Request Tool
              |
              v
        Python Function
              |
              v
         Tool Result
```

---

# Step 5: Tool Results Are Returned

Results are appended as:

```python
{
    "role": "tool",
    "content": json.dumps(result)
}
```

Now the conversation contains:

1. User request
2. Assistant tool call
3. Tool result

---

# Step 6: Final LLM Response

A second LLM call is made:

```python
final_response = client.chat.completions.create(
    model=GROQ_MODEL,
    messages=messages
)
```

Now the model sees:

* Original question
* Tool output

and can generate an informed answer.

---

# Complete Tool Calling Workflow

```text
User Question
      |
      v
      LLM
      |
      |--- Need Tool?
      |
      +------ No ------> Direct Answer
      |
      +------ Yes
                 |
                 v
         Tool Call Request
                 |
                 v
          Python Executes
                 |
                 v
           Tool Result
                 |
                 v
               LLM
                 |
                 v
          Final Response
```

---

# Example: Large Multiplication

Question:

```text
134534423404 * -342343243242
```

Without Tools:

```text
LLM attempts calculation itself
Possibly incorrect
```

With Tools:

```text
LLM calls calculator()
Python computes exact value
LLM returns correct answer
```

---

# Example: Current Information

Question:

```text
Who is Captain of Indian Cricket Team?
```

Without Tools:

```text
Answer depends on training data
May be outdated
```

With Tools:

```text
LLM calls web_search()
Fetches latest information
Returns current answer
```

---

# Key Takeaways

## Without Tool Calling

```text
LLM = Knowledge + Reasoning
```

Strengths:

* Conversation
* Summarization
* Writing
* Reasoning

Weaknesses:

* Current information
* Exact computation
* External actions

---

## With Tool Calling

```text
LLM = Brain
Tools = Hands
```

The model can:

* Search the internet
* Perform accurate calculations
* Query databases
* Call APIs
* Control applications
* Execute workflows

---

# Conclusion

Tool Calling is one of the most important capabilities in modern AI systems.

A standalone LLM can only generate text from its training data.

A tool-enabled LLM can interact with the outside world, retrieve real-time information, perform precise computations, and automate tasks.

This repository demonstrates the fundamental pattern used by modern AI agents:

```text
Think → Decide → Call Tool → Observe → Respond
```

Mastering this pattern is the first step toward building advanced AI agents, assistants, and autonomous systems.
