# Interface Desktop

Cette version ajoute une interface desktop locale au projet multi-agent.

Structure:
- `core.py`: pont entre l'interface et le moteur multi-agent
- `app.py`: interface PySide6

Lancement:

```bash
cd Agent/multimodal-agent
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python 8.Interface/app.py
```

Remarque:
- cette version reutilise le moteur de `7.MultiAgent/multi_agent_version.py`
