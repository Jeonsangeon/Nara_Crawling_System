from PySide6.QtWidgets import *
from PySide6.QtCore import QRect

class MainMenuUi(object):
    def setupUi(self, window: QMainWindow):
        window.setWindowTitle("나라장터 검색 시스템")
        window.setFixedSize(300, 150)
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.notice_search_button = QPushButton(window, text= "입찰 공고 검색")
        font = self.notice_search_button.font()
        font.setPointSize(11)
        font.setBold(True)
        self.notice_search_button.setFont(font)
        self.notice_search_button.setGeometry(QRect(10, 0, 280, 70))

        self.pre_standard_button = QPushButton(window, text= "사전 규격 검색")
        font = self.pre_standard_button.font()
        font.setPointSize(11)
        font.setBold(True)
        self.pre_standard_button.setFont(font)
        self.pre_standard_button.setGeometry(QRect(10, 75, 280, 70))
