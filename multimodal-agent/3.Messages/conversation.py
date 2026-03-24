#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=0.1,
)

conversation = [
    HumanMessage(content="What is RAG?"),
    AIMessage(content="RAG combines retrieval with generation."),
    HumanMessage(content="Why is it useful?"),
]

response = llm.invoke(conversation)
print(response.content)
