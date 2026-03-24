#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=0.1,
)

template = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question clearly:\n{question}",
)

response = llm.invoke(template.format(question="What is RAG?"))
print(response.content)
