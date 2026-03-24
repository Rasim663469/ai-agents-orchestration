#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=0.1,
)

messages = [
    SystemMessage(content="You explain concepts briefly."),
    HumanMessage(content="What is a vector database?"),
]

response = llm.invoke(messages)
print(response.content)
