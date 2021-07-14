from designer.player_ui import Ui_MainWindow
from db_reader import ThemeDB
from theme_grouper import ThemeClassification
from time import sleep
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, Qt, QUrl, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QApplication, QListWidgetItem, QStyle, QMessageBox
from PyQt5.QtGui import QIcon
from os import environ
import sys
import platform
import vlc

environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"

def onPositionChanged(event, window):
    duration = window.vlc_player.get_length()
    position = window.vlc_player.get_time()
    window.playerSlider.setValue(int(window.vlc_player.get_position()*1000))
    window.updatePlayerTimer(position, duration)

def onDurationChanged(event, window):
    duration = window.vlc_player.get_length()
    position = window.vlc_player.get_time()


        
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,classifiedThemes: ThemeClassification, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("AnimeThemes Player")
        self.setWindowIcon(QtGui.QIcon("./assets/img/pepega-logo-small.png"))
        self.loadCategories(classifiedThemes)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.playerWidget)
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()

        self.playerSlider.setMaximum(1000)
        if platform.system() == "Windows":
            self.vlc_player.set_hwnd(int(self.playerWidget.winId()))
        elif platform.system() == "Linux":
            self.vlc_player.set_xwindow(int(self.playerWidget.winId()))
        elif platform.system() == "Darwin":
            self.vlc_player.set_nsobject(int(self.playerWidget.winId()))
        else:
            print("Player not supported")

        self.connectEvents()


    def connectEvents(self):
        self.yearListWidget.itemClicked.connect(self.onYearClick)
        self.videoListWidget.itemClicked.connect(self.onSongClick)
        self.yearListWidget.currentItemChanged.connect(self.onYearChanged)
        self.playButton.clicked.connect(self.onPlayClick)
        self.searchEdit.textChanged.connect(self.onSearchChange)

        self.playerSlider.sliderMoved.connect(self.onSliderMoved)


        self.eventmanager = self.vlc_player.event_manager()
        # The event manager won't work if you use member functions as callback functions
        self.eventmanager.event_attach(vlc.EventType.MediaPlayerPositionChanged, onPositionChanged, self)

    def onSliderMoved(self,position):
        self.vlc_player.set_position(position/1000)

    def onYearClick(self, item):
        key = item.text()
        self.loadVideoList(key)
        
    def onYearChanged(self, item):
        self.videoListWidget.clear()
        self.searchEdit.clear()
        
    def onSearchChange(self):
        text = self.searchEdit.text()
        for i in range(self.videoListWidget.count()):
            item = self.videoListWidget.item(i)
            if text:
                filter = text.lower() in item.text().lower()
                item.setHidden(not filter)
            else:
                item.setHidden(False)
        pass

    def onDurationChanged(self, event):
        #self.playerSlider.setRange(0,duration)
        #self.updatePlayerTimer(0,duration)
        if event.type == vlc.EventType.MediaDurationChanged:
            print("Changed Duration")
            print(f"Time: {self.vlc_player.get_length()}")

    def onSongClick(self, item):
        theme = item.data(Qt.ItemDataRole.UserRole)
        url = theme.getUrl()
        #self.mediaPlayer.setMedia(QMediaContent(QUrl(url)))
        #self.mediaPlayer.play()

        self.songLabel.setText(theme.basename)

        if self.vlc_player.is_playing():
            self.vlc_player.stop()

        self.vlc_player.set_mrl(url)
        self.vlc_player.play()


    def onPlayClick(self):
        if self.vlc_player.is_playing():
            self.vlc_player.set_pause(1)
        else:
            self.vlc_player.play()

    def onError(self):
        # Create message box
        msgBox = QMessageBox()
        msgBox.setIcon((QMessageBox.Warning))
        msgBox.setText("Error message:")
        msgBox.setInformativeText(self.mediaPlayer.errorString())

    def loadCategories(self, tc: ThemeClassification):
        for k in tc.categories:
            self.yearListWidget.addItem(k)

    def loadVideoList(self, key):
        for theme in tc.categories[key]:
            item = QListWidgetItem(theme.filename)
            #item.setText(theme.filename)
            item.setData(Qt.ItemDataRole.UserRole,theme)
            self.videoListWidget.addItem(item)

    def updatePlayerTimer(self, position, duration):
        #p = buildTime(position)
        #d = buildTime(duration)
        self.vidTimeLabel.setText(f"{position/1000} / {duration/1000}")


if __name__ == "__main__":
    db = ThemeDB()
    tc = ThemeClassification()
    tc.addThemes(db.getThemes())
    db.close()

    app = QApplication(sys.argv)

    player = MainWindow(tc)
    player.show()
    sys.exit(app.exec_())