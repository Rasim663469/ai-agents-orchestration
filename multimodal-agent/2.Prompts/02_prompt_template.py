#!/usr/bin/env python3
"""
PromptTemplate - Avec variables dynamiques
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
    model="google/gemma-3-4b-it:free"
)

# Template 
template = PromptTemplate(
    input_variables=["sujet"],
    template="Explique-moi {sujet} en termes simples."
)

# Test avec différents sujets
sujets = ["les agents IA", "RAG", "LLM"]

for sujet in sujets:
    prompt = template.format(sujet=sujet)
    response = llm.invoke(prompt)
    print(f"\n Sujet: {sujet}")
    print(f"Réponse: {response.content}")
    print("-" * 60)
