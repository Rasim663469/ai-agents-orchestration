#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
    model="google/gemma-3-4b-it:free"
)


prompt = "Explane me in one line what is a LLM"
response = llm.invoke(prompt)

print("Question:", prompt)
print("\nRéponse:", response.content)
