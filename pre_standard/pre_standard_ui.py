from PySide6.QtCore import QRect
from PySide6.QtWidgets import *

class PreStandardUi(object):
    def setupUi(self, window: QDialog):
        window.setWindowTitle("사전 규격 검색")  # 창 제목
        window.setFixedSize(490, 90)  # 창 크기
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 창 크기 고정

        # 기관별 검색
        self.agency_label = QLabel(window, text = "기관별검색")
        font = self.agency_label.font()
        font.setBold(True)
        self.agency_label.setFont(font)
        self.agency_label.setGeometry(QRect(10, 0, 70, 30))

        self.announcement_agency_button = QRadioButton(window)
        self.announcement_agency_button.setGeometry(QRect(90, 6, 20, 20))
        self.announcement_agency_label = QLabel(window, text="공고기관")
        self.announcement_agency_label.setGeometry(QRect(110, 0, 50, 30))

        self.demand_agency_button = QRadioButton(window)
        self.demand_agency_button.setGeometry(QRect(165, 6, 20, 20))
        self.demand_agency_button.setChecked(True)
        self.demand_agency_label = QLabel(window, text="수요기관")
        self.demand_agency_label.setGeometry(QRect(185, 0, 50, 30))

        self.agency_line = QLineEdit(window)
        self.agency_line.setGeometry(QRect(240, 0, 240, 25))

        # 업무
        self.work_label = QLabel(window, text="업무")
        font = self.work_label.font()
        font.setBold(True)
        self.work_label.setFont(font)
        self.work_label.setGeometry(QRect(10, 30, 30, 30))

        self.work_all_checkbox = QCheckBox(window)
        self.work_all_checkbox.setGeometry(QRect(90, 36, 20, 20))
        self.work_all_label = QLabel(window, text= "전체")
        self.work_all_label.setGeometry(QRect(110, 30, 30, 30))

        self.work_article_checkbox = QCheckBox(window)
        self.work_article_checkbox.setGeometry(QRect(155, 36, 20, 20))
        self.work_article_label = QLabel(window, text="물품")
        self.work_article_label.setGeometry(QRect(175, 30, 30, 30))

        self.work_construction_checkbox = QCheckBox(window)
        self.work_construction_checkbox.setGeometry(QRect(210, 36, 20, 20))
        self.work_construction_label = QLabel(window, text="공사")
        self.work_construction_label.setGeometry(QRect(230, 30, 30, 30))

        self.work_service_checkbox = QCheckBox(window)
        self.work_service_checkbox.setGeometry(QRect(265, 36, 20, 20))
        self.work_service_label = QLabel(window, text="용역")
        self.work_service_label.setGeometry(QRect(285, 30, 30, 30))
        self.work_service_checkbox.setChecked(True)

        self.work_foreign_checkbox = QCheckBox(window)
        self.work_foreign_checkbox.setGeometry(QRect(320, 36, 20, 20))
        self.work_foreign_label = QLabel(window, text="외자")
        self.work_foreign_label.setGeometry(QRect(340, 30, 30, 30))

        # 품목(사업명)
        self.business_name_label = QLabel(window, text= "품명(사업명)")
        font = self.business_name_label.font()
        font.setBold(True)
        self.business_name_label.setFont(font)
        self.business_name_label.setGeometry(QRect(10, 60, 70, 30))

        self.business_name_line = QLineEdit(window)
        self.business_name_line.setGeometry(QRect(90, 60, 280, 25))

        # 검색
        self.execute_button = QPushButton(window, text="검색")
        self.execute_button.setGeometry(QRect(380, 45, 100, 40))