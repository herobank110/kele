import sys
from PySide6 import QtGui, QtCore, QtWidgets


class DemoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo App")
        self.setGeometry(100, 100, 800, 600)


def main():
    q_app = QtWidgets.QApplication([])
    demo_app = DemoApp()
    demo_app.show()
    sys.exit(q_app.exec_())


if __name__ == "__main__":
    main()
