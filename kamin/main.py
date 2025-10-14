from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from qframelesswindow import FramelessWindow
import os

class Kamin(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.titleBar.raise_()
        self._drag_pos = None

        self.resize(800, 600)

        self.videoWidget = QVideoWidget(self)
        width = 700
        height = 600
        x = 530
        y = 450
        self.videoWidget.setGeometry(width, height, x, y)

        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)

        self.overlay = QLabel(self)
        self.overlay.setPixmap(QPixmap(f"{script_dir}/kamin.png"))
        self.overlay.setScaledContents(True)
        self.overlay.setGeometry(0, 0, 1920, 1080)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoWidget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(f"{script_dir}/kamin.mp4")))
        self.player.setVolume(100)
        self.player.play()

        screen_rect = QApplication.primaryScreen().availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = screen_rect.height() - self.height()
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_P:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
            else:
                self.player.play()
        elif event.key() == Qt.Key_Plus:
            current_volume = self.player.volume()
            new_volume = current_volume + 10
            if new_volume <= 100:
                print(new_volume)
                self.player.setVolume(new_volume)
        elif event.key() == Qt.Key_Minus:
            current_volume = self.player.volume()
            new_volume = current_volume - 10
            if new_volume >= 0:
                self.player.setVolume(new_volume)
        elif event.key() == Qt.Key_M:
            if self.player.volume() > 0:
                self.player.setVolume(0)
            else:
                self.player.setVolume(10)

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "wayland"

    app = QApplication([])
    win = Kamin()
    win.showFullScreen()
    app.exec_()
