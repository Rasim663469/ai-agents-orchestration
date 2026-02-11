# Agent
Brief est une application qui génère un brief clair à partir d’une image et/ou d’un audio (et éventuellement un court texte).
L’utilisateur upload une image (photo, slide, capture) et/ou un audio (note vocale).
L’app extrait les informations clés : description visuelle, texte présent dans l’image (OCR), transcription audio (ASR).
Elle fusionne ces éléments pour produire un brief structuré en Markdown.
Le brief contient : résumé, points clés, détails multimodaux, actions recommandées.
Le système utilise une orchestration “tool-centric” : sélection d’outils experts selon les inputs. 
Objectif : démontrer l’orchestration (séquentiel/parallèle/conditionnel/boucles) et le cycle tool calling.

Version minimale qu'on peut livrer:
Entrées

Image obligatoire (MVP)

Audio optionnel

Texte utilisateur optionnel (“contexte”)

Pipeline MVP (simple)

Image → caption (description courte)

Image → OCR (si du texte existe)

Audio → transcription (si audio fourni)

Fusion → génération du brief (format fixe Markdown)

Sortie MVP (format fixe)

Titre

Résumé (5–8 lignes)

Points clés (5–10 bullets)

Détails image (caption + texte OCR)

Détails audio (transcription + 3 points clés)

Actions recommandées 
