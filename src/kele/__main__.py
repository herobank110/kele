import asyncio
from ollama import AsyncClient


import sys
from PySide6.QtCore import Qt
from PySide6 import QtWidgets


async def chat():
    message = {"role": "user", "content": "Why is the sky blue?"}
    response = await AsyncClient().chat(model="deepseek-r1", messages=[message])
    print(response.content)


def make_searchbar():
    def on_return_pressed():
        print(edit.text())
        edit.setText("")

    frame = QtWidgets.QFrame()
    frame.setLayout(layout := QtWidgets.QHBoxLayout())
    layout.addWidget(
        edit := QtWidgets.QLineEdit(
            placeholderText="Message Kele",
            styleSheet="""
                font-size: 18;
                padding: 10 20;
                border-radius: 13;
            """,
            returnPressed=on_return_pressed
        ),
    )
    return frame


def make_window():
    window = QtWidgets.QMainWindow(windowTitle="kele", centralWidget=QtWidgets.QFrame())
    window.setMinimumSize(800, 600)
    window.centralWidget().setLayout(QtWidgets.QVBoxLayout())
    h = QtWidgets.QLabel(
        "Hey, how can I help?",
        styleSheet="font-size: 32px;",
        alignment=Qt.AlignmentFlag.AlignCenter,
    )
    window.centralWidget().layout().addWidget(h)
    window.centralWidget().layout().addWidget(make_searchbar())
    return window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = make_window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
