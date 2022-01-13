"""
    Main Driver file for the AnimeThemes.moe Video Player

    Created_By: thaivuN

"""


from designer.player_ui import Ui_MainWindow
from db_reader import ThemeDB
from theme_grouper import ThemeClassification
from random_theme import randomTheme

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDir

from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QStyle, QFileDialog

from os import environ
import sys
import platform
import vlc
from enum import Enum
from time import sleep

try:
    unicode
except NameError:
    unicode = str

environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"

class AniMediaType(Enum):
    MRL = 1,
    FILE = 2

# Callback method for VLC
# Update the timer and slider positionm
def onPositionChanged(event, window):
    duration = window.vlc_player.get_length()
    position = window.vlc_player.get_time()
    window.playerSlider.setValue(int(window.vlc_player.get_position()*1000))
    window.updatePlayerTimer(position, duration)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,classifiedThemes: ThemeClassification,app: QApplication, parent=None):
        super().__init__(parent)
        self.classifiedThemes = classifiedThemes
        self.app = app
        self.setupUi(self)
        self.setWindowTitle("AnimeThemes Player")
        self.setWindowIcon(QtGui.QIcon("./assets/img/pepega-logo-small.png"))
        self.loadCategories(classifiedThemes)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(100)
        self.vlc_instance = vlc.Instance()
        self.vlc_player: vlc.MediaPlayer = self.vlc_instance.media_player_new()
        self.vlc_player.audio_set_volume(100)

        self.setStyleSheet("""
            QToolTip{
                background-color: #121212
            }
        
        """)

        self.connectEvents()

        

    # Holds the responsibilty of connecting app events to proper handler functions
    def connectEvents(self):
        self.yearListWidget.itemClicked.connect(self.onYearClick)
        self.videoListWidget.itemClicked.connect(self.onSongClick)
        self.yearListWidget.currentItemChanged.connect(self.onYearChanged)
        self.playButton.clicked.connect(self.onPlayClick)
        self.searchEdit.textChanged.connect(self.onSearchChange)
        self.rdnButton.clicked.connect(self.onPlayRandom)

        self.action_Open.triggered.connect(self.onOpenFile)
        self.actionRandom.triggered.connect(self.onPlayRandom)
        self.actionQuit.triggered.connect(self.onQuit)
        self.fileButton.clicked.connect(self.onOpenFile)
        self.playerSlider.sliderMoved.connect(self.onSliderMoved)
        self.volumeSlider.sliderMoved.connect(self.onVolumeSliderMoved)


        self.eventmanager = self.vlc_player.event_manager()
        # The event manager won't work if you use member functions as callback functions
        self.eventmanager.event_attach(vlc.EventType.MediaPlayerPositionChanged, onPositionChanged, self)

    def onSliderMoved(self,position):
        self.vlc_player.set_position(position/1000)

    # Year column handler
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

    def onSongClick(self, item):
        theme = item.data(Qt.ItemDataRole.UserRole)
        url = theme.getUrl()

        self.setupMedia(url, AniMediaType.MRL)

        self.loadMediaToPlayer(self.media)
        self.media.parse()
        print(f"meta {self.media.get_meta(0)}")
        

        url_tag = f'<a href="{theme.mal_link}">{theme.basename}</a>'
        print(f"url = {url_tag}")
        self.songLabel.setText(url_tag)
        self.songLabel.setToolTip(theme.mal_link)
        #self.songLabel.setText(theme.basename)
        

    def onPlayClick(self):
        if self.vlc_player.is_playing():
            self.vlc_player.set_pause(1)
        else:
            self.vlc_player.play()

    def onVolumeSliderMoved(self, volume):
        self.vlc_player.audio_set_volume(volume)

    def loadCategories(self, tc: ThemeClassification):
        for k in tc.categories:
            self.yearListWidget.addItem(k)

        self.yearListWidget.sortItems(Qt.SortOrder.AscendingOrder)

    def loadVideoList(self, key):
        for theme in tc.categories[key]:
            item = QListWidgetItem(theme.filename)
            item.setData(Qt.ItemDataRole.UserRole, theme)
            item.setToolTip(theme.show_name)
            self.videoListWidget.addItem(item)

        self.videoListWidget.sortItems(Qt.SortOrder.AscendingOrder)

    def updatePlayerTimer(self, position, duration):
        self.vidTimeLabel.setText(f"{position/1000} / {duration/1000}")

    def onOpenFile(self):
        
        print("onOpenFile clicked")
        #self.vlc_player.stop()
        fileName,_ = QFileDialog.getOpenFileName(self, "Open video",QDir.homePath())
        if not fileName:
            return
        if sys.version < '3':
            fileName = unicode(fileName)
        
        self.setupMedia(fileName, AniMediaType.FILE)
        
        #self.vlc_player.set_media(self.media)
        self.media.parse()
        self.loadMediaToPlayer(self.media)
        self.songLabel.setText(self.media.get_meta(0))
        
    def onPlayRandom(self):
        theme = randomTheme(self.classifiedThemes)
        print("onPlayRandom clicked")
        url = theme.getUrl()
        self.setupMedia(url, AniMediaType.MRL)
        
        self.loadMediaToPlayer(self.media)
        self.media.parse()
        
        url_tag = f'<a href="{theme.mal_link}">{theme.basename}</a>'
        print(f"url = {url_tag}")
        self.songLabel.setText(url_tag)
        self.songLabel.setToolTip(theme.mal_link)

        

    def onQuit(self):
        print("onQuit clicked")
        self.close()
        
    def loadMediaToPlayer(self, media):
        self.vlc_player.set_media(media)
        
        self.playerSlider.setMaximum(1000)
        if platform.system() == "Windows":
            self.vlc_player.set_hwnd(int(self.playerWidget.winId()))
        elif platform.system() == "Linux":
            self.vlc_player.set_xwindow(int(self.playerWidget.winId()))
        elif platform.system() == "Darwin":
            self.vlc_player.set_nsobject(int(self.playerWidget.winId()))
        else:
            print("Player not supported")
        sleep(1)
        self.vlc_player.play()


    def setupMedia(self, media, mediaType: AniMediaType):
        if hasattr(self, 'media') and self.media:
            prev_media_name = self.media.get_meta(0)
            if prev_media_name:
                self.vlc_instance.vlm_del_media(prev_media_name)
        if mediaType == AniMediaType.MRL:
            self.media = self.vlc_instance.media_new(mrl = media)
        else:
            self.media = self.vlc_instance.media_new(media)

        

if __name__ == "__main__":
    db = ThemeDB()
    tc = ThemeClassification()
    
    tc.addThemes(db.getThemes())
    db.close()

    app = QApplication(sys.argv)

    player = MainWindow(tc,app)
    player.show()
    sys.exit(app.exec_())