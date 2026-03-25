# Projet Multi-Modal Agent

## Description
Projet academique de progression sur les agents IA.

Le cas d'usage retenu est l'analyse d'images de batiments avec :
- description visuelle
- conversation multi-tour
- RAG documentaire
- version multi-agent
- interface desktop

## Frameworks Et Outils
- Framework principal: LangChain
- LLM principal: Groq
- Vector database: Chroma
- Embeddings: HuggingFace
- Interface desktop: PySide6

## Structure Du Projet
- `1.LLMs/`: premiers tests de modeles
- `2.Prompts/`: prompts simples, templates et mini-projet prompt
- `3.Messages/`: manipulation de messages et conversation
- `4.Agent/`: premier agent simple
- `5.VectorDB/`: embeddings, vector store, retrieval et RAG simple
- `6.AgentAvecRAG/`: agent principal image + RAG
- `7.MultiAgent/`: orchestration multi-agent
- `8.Interface/`: interface desktop locale
- `run_agent.py`: point d'entree rapide vers la version multi-agent terminal
- `requirements.txt`: dependances Python
- `.env.example`: configuration type
- `TEAM.md`: informations equipe
- `PROJECT_PLAN.md`: progression et phases
- `SOURCES.md`: references utilisees

## Versions Disponibles

### 1. Agent Simple
- fichier: `4.Agent/first-agent.py`
- objectif: premier agent minimal

### 2. Agent Avec RAG
- fichier: `6.AgentAvecRAG/rag_conversation_agent.py`
- objectif: analyser une image puis enrichir la reponse avec la knowledge base batiment

### 3. Version Multi-Agent
- fichier: `7.MultiAgent/multi_agent_version.py`
- objectif: decomposer la reponse en plusieurs contributions specialisees avant synthese

### 4. Version Interface Desktop
- dossier: `8.Interface/`
- objectif: utiliser le multi-agent dans une application locale

## Installation

```bash
cd Agent/multimodal-agent
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

## Lancement

### Terminal Multi-Agent
```bash
cd Agent/multimodal-agent
./.venv/bin/python run_agent.py
```

### Agent Avec RAG
```bash
cd Agent/multimodal-agent
./.venv/bin/python 6.AgentAvecRAG/rag_conversation_agent.py
```

### Interface Desktop
```bash
cd Agent/multimodal-agent
./.venv/bin/python 8.Interface/app.py
```

## Knowledge Base
La knowledge base est orientee batiment et contient:
- regles de conformite
- checklist d'inspection
- defauts frequents
- glossaire metier
- cas exemples

## Etat Du Projet
Le projet est structure comme une progression de laboratoire:
- bases LLM
- prompts
- messages
- vector databases
- agent simple
- agent avec RAG
- multi-agent
- interface

Pour les exigences academiques, voir:
- `TEAM.md`
- `PROJECT_PLAN.md`
- `SOURCES.md`
