import asyncio
from ollama import AsyncClient
import sys
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore
import qtawesome


async def chat():
    message = {"role": "user", "content": "Why is the sky blue?"}
    response = await AsyncClient().chat(model="deepseek-r1", messages=[message])
    print(response.content)


def make_input_bar():
    def on_return_pressed():
        print(edit.text())
        edit.setText("")

    frame = QtWidgets.QFrame(
        styleSheet="""
            background-color: #161C2E;
            border: 1px solid #333848;
            border-radius: 23;
        """
    )
    frame.setLayout(layout := QtWidgets.QHBoxLayout())
    layout.addWidget(
        QtWidgets.QPushButton(
            icon=qtawesome.icon("mdi.plus", color="#F2DDCC"),
            iconSize=QtCore.QSize(32, 32),
            styleSheet="""
            QPushButton {
                border: none;
                border-radius: 10;
                padding: 2;
            }
            :hover {
                background-color: #101420;
            }
            """,
        )
    )
    layout.addWidget(
        edit := QtWidgets.QLineEdit(
            placeholderText="Message Copilot",
            styleSheet="""
                padding: 10 20;
                border-radius: 16;
                background-color: #0E131F;
                color: #7E87A6;
                font-size: 18;
                font-family: 'Segoe UI';
                border: none;
            """,
            returnPressed=on_return_pressed,
        ),
    )
    return frame


def make_window():
    window = QtWidgets.QMainWindow(
        windowTitle="kele",
        centralWidget=(
            frame := QtWidgets.QFrame(
                styleSheet="""
                    background-color: #101524;
                """
            )
        ),
    )
    window.setMinimumSize(800, 600)
    frame.setLayout(layout := QtWidgets.QVBoxLayout())
    layout.setContentsMargins(20, 20, 20, 20)
    h = QtWidgets.QLabel(
        "Hey, how can I help?",
        styleSheet="font-size: 32px;",
        alignment=Qt.AlignmentFlag.AlignCenter,
    )
    layout.addWidget(h, 1)
    layout.addWidget(make_input_bar())
    return window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = make_window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
