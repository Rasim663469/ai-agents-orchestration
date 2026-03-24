#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

texts = [
    Document(page_content="A vector database stores embeddings and metadata."),
    Document(page_content="RAG combines retrieval with generation."),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    collection_name="rag_pipeline_demo",
)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=0.1,
)

docs = db.similarity_search("Explain vector databases", k=2)
context = "\n".join(d.page_content for d in docs)

response = llm.invoke(f"Use the context below to answer:\n{context}")
print(response.content)
