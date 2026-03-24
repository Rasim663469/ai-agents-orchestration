#!/usr/bin/env python3

import base64
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain.tools import tool

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_IMAGE_PATH = BASE_DIR.parent.parent / "test" / "test.jpg"

LLM = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    temperature=float(os.getenv("CHAT_TEMPERATURE", "0.1")),
    max_tokens=int(os.getenv("CHAT_MAX_TOKENS", "1000")),
    timeout=int(os.getenv("CHAT_TIMEOUT", "30")),
)


def image_to_data_url(image_path: Path) -> str:
    if not image_path.exists():
        raise FileNotFoundError(f"Image introuvable: {image_path}")

    mime_type, _ = mimetypes.guess_type(image_path.name)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Format non supporte. Utilise une image .png, .jpg ou .jpeg.")

    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


@tool
def detect_objects(image_path: str) -> str:
    """
    Détecte et liste les objets présents dans une image.

    Args:
        image_path: Chemin vers le fichier image
    Returns:
        Liste des objets détectés
    """
    try:
        resolved_path = Path(image_path).expanduser().resolve()
        data_url = image_to_data_url(resolved_path)

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        "Detecte les objets visibles dans cette image. "
                        "Reponds en francais sous forme de liste courte. "
                        "N'invente pas d'objets non visibles."
                    ),
                },
                {"type": "image_url", "image_url": {"url": data_url}},
            ]
        )

        response = LLM.invoke([message])
        return getattr(response, "content", "").strip()
    except Exception as e:
        return f"Erreur lors de l'analyse: {str(e)}"


agent = create_agent(
    model=LLM,
    tools=[detect_objects],
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": f"Analyse l'image située à {DEFAULT_IMAGE_PATH}",
            }
        ]
    }
)


if isinstance(response, dict):
    messages = response.get("messages", [])
else:
    messages = getattr(response, "messages", [])

ai_content = ""
tool_content = []

for msg in messages:
    msg_type = type(msg).__name__
    if msg_type == "AIMessage":
        ai_content += getattr(msg, "content", "")
    elif msg_type == "ToolMessage":
        tool_content.append(getattr(msg, "content", ""))

print("\n--- Réponse de l'IA ---")
print(ai_content)

if tool_content:
    print("\n--- Sortie / Erreurs du tool ---")
    for t in tool_content:
        print(t)
