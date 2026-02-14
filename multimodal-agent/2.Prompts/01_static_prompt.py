#!/usr/bin/env python3
"""
Prompt statique - Sans variable
"""
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    model="meta-llama/llama-3.3-70b-instruct:free"
)

prompt = "Qu'est-ce que LangChain ?"
response = llm.invoke(prompt)

print("Réponse:", response.content)
