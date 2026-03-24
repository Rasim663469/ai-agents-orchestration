#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=0.1,
)

response = llm.invoke([HumanMessage(content="What is an embedding?")])
print(response.content)
