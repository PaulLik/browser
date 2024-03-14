from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QLabel
import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import *
import json


BOOKMARKS = list()


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowIcon(QIcon("./assets/app.ico"))

        # browser
        self.browser = QWebEngineView()
        profile = QWebEngineProfile("storage", self.browser)
        self.browser.setUrl(QUrl("about:blank"))
        self.setCentralWidget(self.browser)

        # bar_navigation
        bar_navigation = QToolBar("Панель навигации")
        self.addToolBar(bar_navigation)
        self.addToolBarBreak()

        btn_back = QAction(QIcon("./assets/back.png"),"Назад", self)
        btn_back.triggered.connect(self.browser.back)
        bar_navigation.addAction(btn_back)

        btn_forward = QAction(QIcon("./assets/forward.png"),"Вперёд", self)
        btn_forward.triggered.connect(self.browser.forward)
        btn_forward.setToolTip("Перейти на страницу вперёд")
        bar_navigation.addAction(btn_forward)

        btn_reload = QAction(QIcon("./assets/reload.png"),"Обновить", self)
        btn_reload.triggered.connect(self.browser.reload)
        bar_navigation.addAction(btn_reload)

        btn_home = QAction(QIcon("./assets/home.png"),"Домой", self)
        btn_home.triggered.connect(lambda: self.browser.setUrl(QUrl("about:blank")))
        bar_navigation.addAction(btn_home)

        self.url_field = QLineEdit()
        self.url_field.returnPressed.connect(self.goto_url)
        bar_navigation.addWidget(self.url_field)

        btn_open_url = QAction(QIcon("./assets/navigate.png"),">>", self)
        btn_open_url.triggered.connect(self.goto_url)
        bar_navigation.addAction(btn_open_url)

        self.search_field = QLineEdit()
        self.search_field.setMaximumWidth(250)
        self.search_field.returnPressed.connect(self.do_search)
        bar_navigation.addWidget(self.search_field)
        
        btn_search = QAction(QIcon("./assets/search.png"),"", self)
        btn_search.triggered.connect(self.do_search)
        bar_navigation.addAction(btn_search)

        # bookmarks
        bar_bookmarks = QToolBar("Панель закладок")
        self.addToolBar(bar_bookmarks)
        bm = QLabel("Ихбранное", self)
        bar_bookmarks.addWidget(bm)
        for bookmark in BOOKMARKS:
            print(bookmark)
            #bm = QAction(bookmark["description"], self)
            #bookmarks.addAction(bm)

        # status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готово")

        self.browser.urlChanged.connect(self.update_url)

        self.showMaximized()

    def goto_url(self):
        if "." in self.url_field.text():
            url = self.url_field.text()
            if not url.startswith("http"):
                url = "http://" + url
            self.browser.setUrl(QUrl(url))
    
    def update_url(self, url):
        self.url_field.setText(url.toString())
    
    def do_search(self):
        if len(self.search_field.text()) > 0:
            searchString = "https://www.google.com/search?q=" +  self.search_field.text().replace(" ", "+")
            self.browser.setUrl(QUrl(searchString))

# End of MainWindow Class


def load_bookmarks():
    with open("./assets/bookmarks.json") as bookmarks_file:
        b = bookmarks_file.read()
        BOOKMARKS = json.loads(b)
        return BOOKMARKS


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_bookmarks()
    app.setApplicationName("LP Browser")
    window = MainWindow()
    window.show()
    app.exec()