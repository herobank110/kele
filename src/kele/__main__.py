import asyncio
from typing import Callable, Literal
from ollama import AsyncClient, chat
import sys
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore, QtAsyncio
import qtawesome


ollama_client = AsyncClient()


IconSize = Literal["small", "large"]


def make_icon_button(
    icon_name: str, size: IconSize = "small", on_click: Callable[[], None] = None
):
    size_px = 24 if size == "small" else 32
    return QtWidgets.QPushButton(
        icon=qtawesome.icon(icon_name, color="#F2DDCC"),
        iconSize=QtCore.QSize(size_px, size_px),
        styleSheet="""
            QPushButton {
                border: none;
                border-radius: 10;
                padding: 2;
            }
            :hover {
                background-color: rgba(0,0,0, 0.4);
            }
        """,
        clicked=on_click,
    )


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
        make_icon_button(icon_name="mdi.plus", size="large", on_click=on_new_chat),
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


def make_chat_bot_message_actions():
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)
    # layout.addWidget(
    #     make_icon_button("mdi.thumb-up", on_click=lambda: print("👍"))
    # )
    # layout.addWidget(
    #     make_icon_button("mdi.thumb-down", on_click=lambda: print("👎"))
    # )
    layout.addWidget(make_icon_button("mdi.content-copy", on_click=lambda: print("📤")))
    return widget


def make_bot_chat_message(text: str):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.addWidget(
        QtWidgets.QLabel(
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
    )
    layout.addWidget(
        make_chat_bot_message_actions(), alignment=Qt.AlignmentFlag.AlignLeft
    )
    return widget


def make_chat_log(chat_history: list[dict]):
    scroll = QtWidgets.QScrollArea(widgetResizable=True)
    scroll.setWidget(inner := QtWidgets.QWidget())
    inner.setLayout(layout := QtWidgets.QVBoxLayout())
    for message in chat_history:
        if message["role"] == "user":
            layout.addWidget(
                make_user_chat_message(message["content"]),
                alignment=Qt.AlignmentFlag.AlignRight,
            )
        else:
            layout.addWidget(make_bot_chat_message(message["content"]))
    # layout.addWidget(
    #     make_user_chat_message("Hello"), alignment=Qt.AlignmentFlag.AlignRight
    # )
    # layout.addWidget(
    #     make_bot_chat_message(
    #         "Hey! It seems like you're really curious about how I'm doing. I'm great, thanks! What's on your mind today? 😊"
    #     )
    # )
    # layout.addWidget(
    #     make_user_chat_message("Hello"), alignment=Qt.AlignmentFlag.AlignRight
    # )
    layout.addStretch(1)
    return scroll


def make_chat_screen():
    chat_history = []
    chat_log_ref = [None]

    def set_chat_history(value: list):
        chat_log_ref[0].setParent(None)
        stack.addWidget(chat_log := make_chat_log(value))
        chat_log_ref[0] = chat_log
        stack.setCurrentIndex(1)

    async def on_enter(text: str):
        chat_history.append({"role": "user", "content": text})
        set_chat_history(chat_history)

        # chat_log_ref[0].setParent(None)
        # stack.addWidget(chat_log := make_chat_log(chat_history))
        # chat_log_ref[0] = chat_log
        # stack.setCurrentIndex(1)

        # chat_history.append({"role": "assistant", "content": "Thinking..."})

        # await asyncio.sleep(0.5)
        # chat_history.append({"role": "assistant", "content": "Thinking..."})
        # return

        chat_future = ollama_client.chat(model="deepseek-r1", messages=chat_history)
        asyncio.ensure_future(chat_future)
        # await asyncio.sleep(0.5)

        # content = (
        #     response.message.content.replace("<think>", "")
        #     .replace("</think>", "")
        #     .strip()
        # )
        content = "yes"
        chat_history.append({"role": "assistant", "content": content})
        set_chat_history(chat_history)

    def on_new_chat():
        chat_history.clear()
        stack.setCurrentIndex(0)

    widget = QtWidgets.QWidget()
    widget.setLayout(layout := QtWidgets.QVBoxLayout())
    layout.setContentsMargins(20, 20, 20, 20)
    layout.addWidget(stack := QtWidgets.QStackedWidget(), stretch=1)
    stack.addWidget(make_how_can_i_help())
    stack.addWidget(chat_log := make_chat_log(chat_history))
    chat_log_ref[0] = chat_log
    layout.addWidget(make_input_bar(on_enter=lambda text: asyncio.ensure_future(on_enter(text)), on_new_chat=on_new_chat))
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
    _app = QtWidgets.QApplication(sys.argv)
    window = make_window()
    window.show()
    QtAsyncio.run(handle_sigint=True)


if __name__ == "__main__":
    main()
