#!/usr/bin/env python3
"""
Agent Multi-Modal avec LangChain + OpenRouter
Orchestre des modèles via API (pas de téléchargement local)
"""
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import base64

# Configuration OpenRouter
OPENROUTER_API_KEY = "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"

# LLM orchestrateur
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model="qwen/qwen3-vl-30b-a3b-thinking",  
    temperature=0.7
)

print("╔═══════════════════════════════════════════════════════════╗")
print("║  Agent Multi-Modal avec OpenRouter                        ║")
print("║  • Description d'images (via API)                         ║")
print("║  • Analyse de contenu                                     ║")
print("╚═══════════════════════════════════════════════════════════╝\n")

def describe_image(image_path: str):
    """Envoie l'image au modèle via OpenRouter"""
    try:
        # Encode l'image en base64
        with open(image_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
        
        print("Envoi de l'image au modèle...")
        
        # Crée le message avec l'image
        messages = [
            SystemMessage(content="Tu es un expert en analyse d'images. Décris en détail ce que tu vois."),
            HumanMessage(
                content=[
                    {"type": "text", "text": "Décris cette image en détail:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            )
        ]
        
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f" Erreur: {e}"

# Interface
while True:
    print("\nMenu:")
    print("  1. Décrire une image")
    print("  2. Quitter")
    
    choice = input("\nVotre choix (1/2): ").strip()
    
    if choice == "1":
        path = input("Chemin de l'image: ").strip()
        result = describe_image(path)
        print(f"\nRéponse:\n{result}\n")
    
    elif choice == "2":
        print("\nAu revoir!\n")
        break
