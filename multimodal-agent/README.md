# Projet Multi-Modal Agent - LangChain

## Description
Projet académique sur l'orchestration d'agents IA utilisant le framework LangChain.

**Objectif :** Créer une application multi-modale capable de :
- Décrire des images
- Orchestrer différents agents IA spécialisés

## Framework choisi
- **LangChain** / **LangGraph**
- **OpenRouter** (API gratuite pour LLMs)

## Structure du projet
- `run_agent.py`: fichier main
- `1.LLMs/`: notes ou essais de modeles
- `2.Prompts/`: scripts simples d'apprentissage LangChain
- `3.Agent/first-agent.py`: premier exemple d'agent
- `4.AgentAvecRAG/rag_conversation_agent.py`: agent principal image + RAG
- `4.AgentAvecRAG/knowledge_base/`: documents utilises par le RAG
- `5.MultiAgent/multi_agent_image_rag.py`: version multi-agent
- `../test/`: images de test
- `.venv/`: unique environnement virtuel du projet


Lancement:

```bash
cd Agent/multimodal-agent
cp .env.example .env
./.venv/bin/python run_agent.py
```

Notes:
- Le script demande un chemin d'image puis ouvre une conversation sur cette image.
- Le chat conserve le contexte de la session pour les questions suivantes.
- Utilise un modele multimodal Groq pour l'analyse d'image.
- Le RAG lit les documents du dossier `4.AgentAvecRAG/knowledge_base/`.
- Les formats supportes par defaut sont `.txt`, `.md`, `.csv`, `.json` et `.pdf`.
- Le RAG utilise par defaut `HuggingFaceEmbeddings` avec `sentence-transformers/all-MiniLM-L6-v2`.
- Le vector store utilise Chroma

## Version Multi-Agent

Lancement:

```bash
cd Agent/multimodal-agent
./.venv/bin/python 5.MultiAgent/rag_conversation_agent.py
```

Principe:
- cette version repart du socle `4.AgentAvecRAG/rag_conversation_agent.py`
- une contribution specialisee detaille l'analyse visuelle
- une contribution specialisee applique le RAG metier
- une synthese finale fusionne les deux

Ce que fait la version multi-agent en interne :

- un bloc produit la description visuelle
- un bloc enrichit l’analyse détaillée
- un bloc applique le contexte RAG bâtiment
- un bloc final fusionne tout en une seule réponse

## Dependance

Installation dans un nouvel environnement:

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```
