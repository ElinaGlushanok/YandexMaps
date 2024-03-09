import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('map1.ui', self)
        self.map_zoom = 5
        self.map_ll = [45, 45]
        self.map_l = 'map'
        self.map_key = ''
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get('https://static-maps.yandex.ru/1.x/',
                                params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.g_map.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key == Qt.Key_PageUp:
            self.map_zoom += 1
        elif event.key == Qt.Key_PageDown:
            self.map_zoom -= 1
        if self.map_zoom < 1:
            self.map_zoom = 1
        elif self.map_zoom > 10:
            self.map_zoom = 10
        self.refresh_map()


app = QApplication(sys.argv)
map = MainWindow()
map.show()
sys.exit(app.exec())
