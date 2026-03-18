#!/usr/bin/env python3
"""
Premier test simple avec LangChain + OpenRouter
Objectif: Vérifier que tout fonctionne avec un prompt basique
"""
from langchain_openai import ChatOpenAI

# Configuration
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
    model="meta-llama/llama-3.3-70b-instruct:free"
)

# Prompt simple
prompt = "Explique-moi en une phrase ce qu'est un LLM."
response = llm.invoke(prompt)

print("Question:", prompt)
print("\nRéponse:", response.content)
