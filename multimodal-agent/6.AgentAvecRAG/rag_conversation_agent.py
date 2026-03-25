#!/usr/bin/env python3

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_IMAGE_PATH = BASE_DIR.parent.parent / "test" / "Maison.jpeg"
DEFAULT_KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
DEFAULT_CHROMA_DIR = BASE_DIR / ".chroma"


def build_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Ajoute GROQ_API_KEY dans ton fichier .env.")

    return ChatGroq(
        api_key=api_key,
        model=os.getenv(
            "VISION_MODEL",
            "meta-llama/llama-4-scout-17b-16e-instruct",
        ),
        temperature=float(os.getenv("CHAT_TEMPERATURE", "0.1")),
        max_tokens=int(os.getenv("CHAT_MAX_TOKENS", "1000")),
        timeout=int(os.getenv("CHAT_TIMEOUT", "30")),
    )


def build_embeddings():
    embeddings_provider = os.getenv("EMBEDDINGS_PROVIDER", "huggingface").lower()

    if embeddings_provider == "huggingface":
        # Ici on transforme les chunks de documents en vecteurs pour la recherche semantique.
        return HuggingFaceEmbeddings(
            model_name=os.getenv(
                "HUGGINGFACE_EMBEDDINGS_MODEL",
                "sentence-transformers/all-MiniLM-L6-v2",
            )
        )

    api_key = os.getenv("EMBEDDINGS_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Ajoute EMBEDDINGS_API_KEY ou OPENAI_API_KEY dans ton fichier .env."
        )

    return OpenAIEmbeddings(
        base_url=os.getenv("EMBEDDINGS_BASE_URL"),
        api_key=api_key,
        model=os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small"),
        timeout=int(os.getenv("EMBEDDINGS_TIMEOUT", "30")),
    )


def image_to_data_url(image_path: Path) -> str:
    if not image_path.exists():
        raise FileNotFoundError(f"Image introuvable: {image_path}")

    mime_type, _ = mimetypes.guess_type(image_path.name)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(
            "Format non supporte. Utilise une image .png, .jpg, .jpeg, .webp ou .gif."
        )

    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_pdf_file(path: Path) -> str:
    loader = PyPDFLoader(str(path))
    documents = loader.load()
    return "\n".join(doc.page_content for doc in documents)


def load_documents(knowledge_dir: Path) -> list[Document]:
    supported_suffixes = {".txt", ".md", ".csv", ".json", ".pdf"}
    documents: list[Document] = []

    if not knowledge_dir.exists():
        raise FileNotFoundError(
            f"Le dossier de connaissances est introuvable: {knowledge_dir}"
        )

    for path in sorted(knowledge_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in supported_suffixes:
            continue

        if path.suffix.lower() == ".pdf":
            content = load_pdf_file(path)
        else:
            content = load_text_file(path)

        if not content.strip():
            continue

        documents.append(
            Document(
                page_content=content,
                metadata={"source": str(path.relative_to(knowledge_dir.parent))},
            )
        )

    if not documents:
        raise ValueError(
            f"Aucun document exploitable trouvé dans {knowledge_dir}. "
            "Ajoute des fichiers .txt, .md, .csv, .json ou .pdf."
        )

    return documents


def split_documents(documents: Iterable[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(os.getenv("RAG_CHUNK_SIZE", "500")),
        chunk_overlap=int(os.getenv("RAG_CHUNK_OVERLAP", "100")),
    )
    return splitter.split_documents(list(documents))


def build_retriever(knowledge_dir: Path):
    documents = load_documents(knowledge_dir)
    chunks = split_documents(documents)
    embeddings = build_embeddings()
    persist_directory = Path(
        os.getenv("CHROMA_DIR", str(DEFAULT_CHROMA_DIR))
    ).resolve()
    persist_directory.mkdir(parents=True, exist_ok=True)

    # On stocke les embeddings dans Chroma pour pouvoir retrouver ensuite
    # les passages les plus utiles par similarite.
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=os.getenv("CHROMA_COLLECTION", "rag_collection"),
        persist_directory=str(persist_directory),
    )

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": int(os.getenv("RAG_TOP_K", "2")),
            "fetch_k": int(os.getenv("RAG_FETCH_K", "8")),
            "lambda_mult": float(os.getenv("RAG_LAMBDA_MULT", "0.5")),
        },
    )


def format_docs(docs: list[Document]) -> str:
    if not docs:
        return "Aucun document pertinent trouvé."

    sections = []
    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "source inconnue")
        sections.append(f"[Source {index}: {source}]\n{doc.page_content.strip()}")
    return "\n\n".join(sections)


def format_history(history: list[tuple[str, str]]) -> str:
    if not history:
        return "Aucun historique."
    return "\n".join(f"{role}: {content}" for role, content in history)


def describe_image(llm: ChatGroq, image_path: Path) -> str:
    data_url = image_to_data_url(image_path)

    # Premiere etape: on demande au modele vision une description propre de l'image.
    # Cette description servira ensuite de base a toute la conversation.
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "Decris cette image en detail. "
                    "Commence par une vue d'ensemble, puis liste les elements visibles. "
                    "Signale les details incertains."
                ),
            },
            {"type": "image_url", "image_url": {"url": data_url}},
        ]
    )

    response = llm.invoke([message])
    return getattr(response, "content", "").strip()


def build_rag_chain(llm: ChatGroq, retriever):
    prompt = PromptTemplate(
        template="""
Tu es un agent d'analyse d'image avec RAG.

Utilise les informations suivantes pour repondre:
- Description de l'image: {image_description}
- Historique de conversation: {history}
- Contexte documentaire: {context}

Regles:
- Reponds d'abord a partir de l'image.
- Utilise le contexte documentaire seulement s'il est pertinent.
- Cite les sources quand tu utilises le contexte documentaire.
- Si l'information n'est ni dans l'image ni dans le contexte, dis clairement que tu ne sais pas.
- Reponds en francais sauf si l'utilisateur demande une autre langue.

Question: {question}
""".strip(),
        input_variables=["image_description", "history", "context", "question"],
    )

    parser = StrOutputParser()

    # A chaque question, on reconstruit la reponse a partir de trois sources:
    # l'image de depart, l'historique de conversation et les documents retrouves par le retriever.
    return (
        {
            # C'est ici que le RAG interroge la base vectorielle pour recuperer
            # les extraits les plus pertinents par rapport a la question.
            "context": RunnableLambda(
                lambda x: format_docs(retriever.invoke(x["question"]))
            ),
            "question": RunnableLambda(lambda x: x["question"]),
            "history": RunnableLambda(lambda x: x["history"]),
            "image_description": RunnableLambda(lambda x: x["image_description"]),
        }
        | prompt
        | llm
        | parser
    )


def main() -> None:
    try:
        print("Initialisation du modele Groq...", flush=True)
        llm = build_llm()
        knowledge_dir_value = os.getenv("KNOWLEDGE_DIR") or str(DEFAULT_KNOWLEDGE_DIR)
        knowledge_dir = Path(knowledge_dir_value).resolve()
        print(f"Chargement des documents RAG depuis: {knowledge_dir}", flush=True)
        # On prepare ici toute la partie documentaire: chargement, embeddings,
        # base vectorielle et retriever.
        retriever = build_retriever(knowledge_dir)
        rag_chain = build_rag_chain(llm, retriever)
    except Exception as exc:
        print(f"Erreur d'initialisation: {exc}")
        return

    raw_image_path = input(f"Chemin de l'image [{DEFAULT_IMAGE_PATH}] > ").strip()
    image_path = (
        Path(raw_image_path).expanduser().resolve()
        if raw_image_path1. Expliquer la mémoire + chat
Tu dis quelque chose comme :

“Dans cette partie, on montre comment une conversation peut être conservée dans le temps. L’idée est que l’agent ne répond pas seulement à une question isolée, mais qu’il garde l’historique des échanges pour comprendre le contexte.”

Puis tu montres dans conversation.py :

HumanMessage
AIMessage
la liste conversation
llm.invoke(conversation)
Message à faire passer :

la mémoire ici est représentée par l’historique des messages
plus tard, ce principe est repris dans AgentAvecRAG avec history
        else DEFAULT_IMAGE_PATH.resolve()
    )

    try:
        print(f"Lecture de l'image: {image_path}", flush=True)
        image_description = describe_image(llm, image_path)
    except Exception as exc:
        print(f"Erreur pendant l'analyse de l'image: {exc}")
        return

    if not image_description:
        image_description = "Aucune description n'a pu etre generee."

    print("\n--- Description initiale de l'image ---")
    print(image_description)
    print()

    # On garde une trace de la conversation pour que les questions suivantes
    # restent contextualisees et ne repartent pas de zero.
    history: list[tuple[str, str]] = [("assistant", image_description)]

    print("Conversation ouverte sur cette image.")
    print(f"Base RAG: {knowledge_dir}")
    print("Pose des questions sur l'image ou tape `exit` pour quitter.\n")

    while True:
        try:
            user_input = input("Vous > ").strip()
        except KeyboardInterrupt:
            print("\nFin de la conversation.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Fin de la conversation.")
            break

        payload = {
            "question": user_input,
            "history": format_history(history),
            "image_description": image_description,
        }

        try:
            # La reponse finale combine l'image, l'historique et le contexte RAG.
            answer = rag_chain.invoke(payload).strip()
        except Exception as exc:
            print(f"\nErreur pendant la generation: {exc}\n")
            continue

        print(f"\nAgent > {answer}\n")
        # On enregistre chaque tour pour garder une vraie conversation suivie.
        history.append(("user", user_input))
        history.append(("assistant", answer))


if __name__ == "__main__":
    main()
