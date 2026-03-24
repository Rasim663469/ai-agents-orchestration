#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
MULTI_AGENT_PATH = PROJECT_DIR / "7.MultiAgent" / "multi_agent_version.py"


def load_multi_agent_module():
    spec = importlib.util.spec_from_file_location(
        "multi_agent_version",
        MULTI_AGENT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Impossible de charger le module multi-agent.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MultiAgentService:
    def __init__(self) -> None:
        self.module = load_multi_agent_module()
        self.llm = self.module.build_llm()
        knowledge_dir_value = (
            self.module.os.getenv("MULTI_KNOWLEDGE_DIR")
            or str(self.module.DEFAULT_KNOWLEDGE_DIR)
        )
        self.knowledge_dir = Path(knowledge_dir_value).resolve()
        self.retriever = self.module.build_retriever(self.knowledge_dir)
        self.rag_chain = self.module.build_multi_agent_chain(self.llm, self.retriever)

    def analyze_image(self, image_path: str) -> str:
        return self.module.describe_image(self.llm, Path(image_path).resolve())

    def answer(self, image_description: str, history_pairs: list[tuple[str, str]], question: str) -> str:
        payload = {
            "question": question,
            "history": self.module.format_history(history_pairs),
            "image_description": image_description,
        }
        return self.rag_chain.invoke(payload).strip()
