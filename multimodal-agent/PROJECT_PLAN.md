# Project Plan

## Use Case
Application d'analyse d'image dans le domaine du batiment, enrichie par RAG, multi-agent et interface desktop.

Le projet a commence comme une analyse d'image generaliste. La specialisation progressive vers le batiment a ete choisie pendant le developpement pour donner un cadre metier precis au systeme, structurer une knowledge base pertinente, et rendre plus utile l'introduction du RAG, du multi-agent et de l'interface finale.

## Framework Choice
- Framework principal: LangChain
- LLM principal: Groq
- Vector database: Chroma
- Embeddings: HuggingFace
- Interface: PySide6

## Progression Pedagogique
- `1.LLMs`: premiers appels a des modeles et verification de l'environnement
- `2.Prompts`: static_prompt, dynamic_prompt, chat_prompt et mini projet prompt
- `3.Messages`: messages simples, messages avec roles et conversation multi-tour
- `4.Agent`: premier agent simple
- `5.VectorDB`: embeddings, stockage vectoriel, retrieval et pipeline RAG simple
- `6.AgentAvecRAG`: agent d'analyse d'image avec RAG complet
- `7.MultiAgent`: decomposition du raisonnement en plusieurs contributions specialisees
- `8.Interface`: application desktop locale

## Laboratoires Et Phases
- Labo 1:
  phases couvertes: LLMs + Prompts
- Labo 2:
  phases couvertes: Messages + Agent simple
- Labo 3:
  phases couvertes: VectorDB + Agent avec RAG
- Labo 4:
  phases couvertes: Multi-agent
- Labo 5:
  phases couvertes: Interface

## Experiments
- modeles testes: OpenRouter, Groq
- approches testees: agent simple, RAG, multi-agent, interface web locale puis desktop
- use case retenu: analyse visuelle de batiments
