#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core import MultiAgentService


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Multi-Agent Batiment")
        self.resize(1280, 820)

        self.service = MultiAgentService()
        self.image_path: str = ""
        self.image_description: str = ""
        self.history_pairs: list[tuple[str, str]] = []

        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        header = QLabel("Analyse d'image batiment avec multi-agent")
        header.setStyleSheet("font-size: 24px; font-weight: 700;")
        layout.addWidget(header)

        subheader = QLabel(
            "Charge une image, lance l'analyse initiale, puis pose des questions. "
            "Le systeme combine vision, specialisation metier et RAG."
        )
        subheader.setWordWrap(True)
        layout.addWidget(subheader)

        controls = QHBoxLayout()
        self.path_label = QLabel("Aucune image selectionnee")
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        select_button = QPushButton("Choisir une image")
        analyze_button = QPushButton("Analyser l'image")
        clear_button = QPushButton("Reinitialiser")

        select_button.clicked.connect(self.select_image)
        analyze_button.clicked.connect(self.analyze_image)
        clear_button.clicked.connect(self.reset_session)

        controls.addWidget(select_button)
        controls.addWidget(analyze_button)
        controls.addWidget(clear_button)
        controls.addWidget(self.path_label, 1)
        layout.addLayout(controls)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter, 1)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.image_preview = QLabel("Apercu image")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setMinimumHeight(360)
        self.image_preview.setStyleSheet(
            "border: 1px solid #444; background: #111; color: #ddd;"
        )
        self.description_box = QPlainTextEdit()
        self.description_box.setPlaceholderText("La description initiale apparaitra ici.")
        self.description_box.setReadOnly(True)
        left_layout.addWidget(self.image_preview, 2)
        left_layout.addWidget(QLabel("Description initiale"))
        left_layout.addWidget(self.description_box, 1)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setPlaceholderText("La conversation apparaitra ici.")
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Pose une question, par exemple: Vois-tu des defauts visibles sur la facade ?"
        )
        send_button = QPushButton("Envoyer")
        send_button.clicked.connect(self.send_question)
        self.question_input.returnPressed.connect(self.send_question)

        question_row = QHBoxLayout()
        question_row.addWidget(self.question_input, 1)
        question_row.addWidget(send_button)

        right_layout.addWidget(QLabel("Conversation"))
        right_layout.addWidget(self.chat_box, 1)
        right_layout.addLayout(question_row)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([520, 760])

        footer = QLabel(
            f"Base RAG: {self.service.knowledge_dir}"
        )
        footer.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(footer)

    def select_image(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une image",
            str(Path.home()),
            "Images (*.png *.jpg *.jpeg *.webp *.gif)",
        )
        if not file_path:
            return

        self.image_path = file_path
        self.path_label.setText(file_path)
        self._update_preview(file_path)

    def _update_preview(self, file_path: str) -> None:
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.image_preview.setText("Impossible de charger l'image")
            return

        scaled = pixmap.scaled(
            520,
            420,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_preview.setPixmap(scaled)

    def analyze_image(self) -> None:
        if not self.image_path:
            QMessageBox.warning(self, "Image manquante", "Choisis d'abord une image.")
            return

        try:
            self.statusBar().showMessage("Analyse de l'image en cours...")
            QApplication.processEvents()
            self.image_description = self.service.analyze_image(self.image_path)
            self.description_box.setPlainText(self.image_description)
            self.chat_box.clear()
            self._append_chat("Assistant", self.image_description)
            self.history_pairs = [("assistant", self.image_description)]
            self.statusBar().showMessage("Analyse terminee.", 5000)
        except Exception as exc:
            self.statusBar().clearMessage()
            QMessageBox.critical(
                self,
                "Erreur d'analyse",
                str(exc),
            )

    def send_question(self) -> None:
        question = self.question_input.text().strip()
        if not question:
            return
        if not self.image_description:
            QMessageBox.warning(
                self,
                "Analyse requise",
                "Analyse d'abord une image avant de poser une question.",
            )
            return

        try:
            self.statusBar().showMessage("Generation de la reponse...")
            QApplication.processEvents()
            self._append_chat("Vous", question)
            answer = self.service.answer(self.image_description, self.history_pairs, question)
            self.history_pairs.append(("user", question))
            self.history_pairs.append(("assistant", answer))
            self._append_chat("Assistant", answer)
            self.question_input.clear()
            self.statusBar().showMessage("Reponse terminee.", 5000)
        except Exception as exc:
            self.statusBar().clearMessage()
            QMessageBox.critical(self, "Erreur", str(exc))

    def reset_session(self) -> None:
        self.image_path = ""
        self.image_description = ""
        self.history_pairs = []
        self.path_label.setText("Aucune image selectionnee")
        self.image_preview.clear()
        self.image_preview.setText("Apercu image")
        self.description_box.clear()
        self.chat_box.clear()
        self.question_input.clear()
        self.statusBar().showMessage("Session reinitialisee.", 3000)

    def _append_chat(self, speaker: str, message: str) -> None:
        safe_message = message.replace("\n", "<br>")
        self.chat_box.append(f"<b>{speaker}:</b><br>{safe_message}<br>")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
