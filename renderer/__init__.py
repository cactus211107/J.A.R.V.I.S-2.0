import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer

def setWordsList(words:list[str]):pass

class GraphicsThread(QThread):
    update_signal = pyqtSignal()
    def __init__(self, parent: QObject | None = None) -> None:
        self.app = QApplication(sys.argv)
        QThread.__init__(self, parent=parent)
    def run(self):
        print('run')
        self.window = QWidget()
        self.label = QLabel('Hello, visual feedback!')
        self.label.move(50, 50)
        self.label.show()
        QTimer.singleShot(5000, self.app.quit)  # Quit after 5 seconds
        self.app.exec_()

# Create and start the thread
thread = GraphicsThread()
thread.start()
