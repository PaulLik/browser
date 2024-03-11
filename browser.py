from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QWidget
import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowIcon(QIcon("app.ico"))
        self.browser = QWebEngineView()
        profile = QWebEngineProfile("storage", self.browser)
        self.browser.setUrl(QUrl("https://www.google.ru"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        btn_back = QAction(QIcon("back.png"),"Назад", self)
        btn_back.triggered.connect(self.browser.back)
        navbar.addAction(btn_back)

        btn_forward = QAction(QIcon("forward.png"),"Вперёд", self)
        btn_forward.triggered.connect(self.browser.forward)
        btn_forward.setToolTip("Перейти на страницу вперёд")
        navbar.addAction(btn_forward)

        btn_reload = QAction(QIcon("reload.png"),"Обновить", self)
        btn_reload.triggered.connect(self.browser.reload)
        navbar.addAction(btn_reload)

        btn_home = QAction(QIcon("home.png"),"Домой", self)
        btn_home.triggered.connect(lambda: self.browser.setUrl(QUrl("about:blank")))
        navbar.addAction(btn_home)

        self.url_field = QLineEdit()
        self.url_field.returnPressed.connect(self.goto_url)
        navbar.addWidget(self.url_field)

        btn_open_url = QAction(QIcon("navigate.png"),">>", self)
        btn_open_url.triggered.connect(self.goto_url)
        navbar.addAction(btn_open_url)

        self.search_field = QLineEdit()
        self.search_field.setMaximumWidth(250)
        self.search_field.returnPressed.connect(self.do_search)
        navbar.addWidget(self.search_field)
        
        btn_search = QAction(QIcon("search.png"),"", self)
        btn_search.triggered.connect(self.do_search)
        navbar.addAction(btn_search)

        self.browser.urlChanged.connect(self.update_url)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("LP Browser")
    window = MainWindow()
    window.show()
    app.exec()