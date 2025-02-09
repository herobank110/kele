import asyncio
from typing import Callable
from ollama import AsyncClient
import sys
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore
import qtawesome


async def chat():
    message = {"role": "user", "content": "Why is the sky blue?"}
    response = await AsyncClient().chat(model="deepseek-r1", messages=[message])
    print(response.content)


def make_input_bar(
    on_new_chat: Callable[[], None],
    on_enter: Callable[[str], None],
):
    def on_return_pressed():
        text = edit.text()
        edit.setText("")
        on_enter(text)

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
            clicked=on_new_chat,
        )
    )
    layout.addWidget(
        edit := QtWidgets.QLineEdit(
            placeholderText="Message Copilot",
            styleSheet="""
                padding: 10 15;
                border-radius: 18;
                background-color: #0E131F;
                placeholder-text-color: #7E87A6;
                color: #F1F1F2;
                font-size: 12pt;
                font-family: 'Segoe UI';
                border: none;
            """,
            returnPressed=on_return_pressed,
        ),
    )
    return frame


def make_how_can_i_help():
    return QtWidgets.QLabel(
        text="Hey, how can I help?",
        styleSheet="font-size: 32px;",
        alignment=Qt.AlignmentFlag.AlignCenter,
    )


def make_user_chat_message(text: str):
    return QtWidgets.QLabel(
        text=text,
        styleSheet="""
                background-color: #1D2439;
                color: #F2DDCC;
                padding: 10;
                border-radius: 10;
                font-size: 12pt;
                font-family: 'Segoe UI';
            """,
        wordWrap=True,
        textInteractionFlags=Qt.TextInteractionFlag.TextBrowserInteraction,
        sizePolicy=QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        ),
    )


def make_bot_chat_message(text: str):
    return QtWidgets.QLabel(
        text=text,
        styleSheet="""
            color: #F2DDCC;
            padding: 10;
            border-radius: 10;
            font-size: 12pt;
            font-family: 'Segoe UI';
        """,
        wordWrap=True,
        textInteractionFlags=Qt.TextInteractionFlag.TextBrowserInteraction,
    )


def make_chat_log():
    scroll = QtWidgets.QScrollArea(widgetResizable=True)
    scroll.setWidget(inner := QtWidgets.QWidget())
    inner.setLayout(layout := QtWidgets.QVBoxLayout())
    layout.addWidget(
        make_user_chat_message("Hello"), alignment=Qt.AlignmentFlag.AlignRight
    )
    layout.addWidget(
        make_bot_chat_message(
            "Hey! It seems like you're really curious about how I'm doing. I'm great, thanks! What's on your mind today? 😊"
        )
    )
    layout.addWidget(
        make_user_chat_message("Hello"), alignment=Qt.AlignmentFlag.AlignRight
    )
    layout.addStretch(1)
    return scroll


def make_chat_screen():
    chat_history = []

    def on_enter(text: str):
        stack.setCurrentIndex(1)
        print("Hello", text)

    def on_new_chat():
        chat_history = []
        stack.setCurrentIndex(0)

    widget = QtWidgets.QWidget()
    widget.setLayout(layout := QtWidgets.QVBoxLayout())
    layout.setContentsMargins(20, 20, 20, 20)
    layout.addWidget(stack := QtWidgets.QStackedWidget(), stretch=1)
    stack.addWidget(make_how_can_i_help())
    stack.addWidget(make_chat_log())
    stack.setCurrentIndex(1)
    layout.addWidget(make_input_bar(on_enter=on_enter, on_new_chat=on_new_chat))
    return widget


def make_window():
    window = QtWidgets.QMainWindow(
        windowTitle="kele",
        centralWidget=(
            frame := QtWidgets.QFrame(
                styleSheet="""
                    background-color: #101524;
                """,
            )
        ),
    )
    window.setMinimumSize(800, 600)
    frame.setLayout(layout := QtWidgets.QVBoxLayout())
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(make_chat_screen())
    return window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = make_window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
