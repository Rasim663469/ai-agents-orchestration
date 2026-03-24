#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=0.1,
)

messages = [
    SystemMessage(content="Tu es un assistant concis qui explique les concepts simplement."),
    HumanMessage(content="Explique en deux phrases ce qu'est une conversation multi-tour."),
]

response = llm.invoke(messages)
print(response.content)
