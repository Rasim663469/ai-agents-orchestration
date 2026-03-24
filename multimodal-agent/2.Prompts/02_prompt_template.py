#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=float(os.getenv("CHAT_TEMPERATURE", "0.1")),
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
