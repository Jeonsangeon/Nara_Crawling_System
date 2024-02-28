from main_menu.main_menu_ui import MainMenuUi
from notice_search.notice_search import NoticeSearch
from pre_standard.pre_standard import PreStandard
from PySide6.QtWidgets import QMainWindow

class MainMenu(QMainWindow, MainMenuUi):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.notice_search_button.clicked.connect(self.open_notice_search)
        self.pre_standard_button.clicked.connect(self.open_pre_standard)

    def open_notice_search(self):
        Dialog = NoticeSearch()
        Dialog.exec()

    def open_pre_standard(self):
        Dialog = PreStandard()
        Dialog.exec()