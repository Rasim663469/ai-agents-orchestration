#!/usr/bin/env python3
"""
Premier test simple avec LangChain + OpenRouter
Objectif: Vérifier que tout fonctionne avec un prompt basique
"""
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
    model="google/gemma-3-4b-it:free"
)


prompt = "Explane me in one line what is a LLM"
response = llm.invoke(prompt)

print("Question:", prompt)
print("\nRéponse:", response.content)
