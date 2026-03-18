import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from PIL import Image

load_dotenv()

LLM = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
    model="meta-llama/llama-3.3-70b-instruct:free",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)

@tool
def detect_objects(image_path: str) -> str:
    """
    Détecte et liste les objets présents dans une image.

    Args:
        image_path: Chemin vers le fichier image 
    Returns:
        Liste des objets détectés avec leur niveau de confiance
    """
    try:
        # Juste pour test : vérifier si l'image existe
        image = Image.open(image_path)
        return f"L'image '{image_path}' est accessible. (Détection d'objets simulée)"
    except Exception as e:
        return f"Erreur lors de l'analyse: {str(e)}"

agent = create_agent(
    model=LLM,
    tools=[detect_objects],
)

response = agent.invoke({
    "messages": [
        {"role": "user", "content": "Analyse l'image située à ../../test/test.jpg"}
    ]
})


# Récupération sécurisée des messages
if isinstance(response, dict):
    messages = response.get("messages", [])
else:
    messages = getattr(response, "messages", [])

ai_content = ""
tool_content = []

for msg in messages:
    # Selon le type du message
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
