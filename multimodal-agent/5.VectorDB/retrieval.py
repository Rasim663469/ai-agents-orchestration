#!/usr/bin/env python3

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


texts = [
    Document(page_content="LLMs generate text."),
    Document(page_content="Vector DBs store embeddings."),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    collection_name="retrieval_demo",
)

query = "What stores embeddings?"
docs = db.similarity_search(query, k=1)

print(docs[0].page_content)
