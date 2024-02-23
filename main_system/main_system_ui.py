from PySide6.QtCore import QRect
from PySide6.QtWidgets import *

class MainSystemUi(object):
    def setupUi(self, window: QMainWindow):
        window.setWindowTitle("통합 DB 작업")  # 창 제목
        window.setFixedSize(560, 130)  # 창 크기
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 창 크기 고정
        
        # 업무
        self.work_label = QLabel(window)
        self.work_label.setText("업무")
        self.work_label.setGeometry(QRect(10, 0, 30, 30))

        self.work_all_checkbox = QCheckBox(window)
        self.work_all_checkbox.setGeometry(QRect(45, 6, 20, 20))
        self.work_all_label = QLabel(window)
        self.work_all_label.setText("전체")
        self.work_all_label.setGeometry(QRect(65, 0, 30, 30))

        self.work_article_checkbox = QCheckBox(window)
        self.work_article_checkbox.setGeometry(QRect(110, 6, 20, 20))
        self.work_article_label = QLabel(window)
        self.work_article_label.setText("물품")
        self.work_article_label.setGeometry(QRect(130, 0, 30, 30))

        self.work_construction_checkbox = QCheckBox(window)
        self.work_construction_checkbox.setGeometry(QRect(165, 6, 20, 20))
        self.work_construction_label = QLabel(window)
        self.work_construction_label.setText("공사")
        self.work_construction_label.setGeometry(QRect(185, 0, 30, 30))

        self.work_service_checkbox = QCheckBox(window)
        self.work_service_checkbox.setGeometry(QRect(220, 6, 20, 20))
        self.work_service_label = QLabel(window)
        self.work_service_label.setText("용역")
        self.work_service_label.setGeometry(QRect(240, 0, 30, 30))
        self.work_service_checkbox.setChecked(True)

        self.work_lease_checkbox = QCheckBox(window)
        self.work_lease_checkbox.setGeometry(QRect(275, 6, 20, 20))
        self.work_lease_label = QLabel(window)
        self.work_lease_label.setText("리스")
        self.work_lease_label.setGeometry(QRect(295, 0, 30, 30))

        self.work_foreign_checkbox = QCheckBox(window)
        self.work_foreign_checkbox.setGeometry(QRect(330, 6, 20, 20))
        self.work_foreign_label = QLabel(window)
        self.work_foreign_label.setText("외자")
        self.work_foreign_label.setGeometry(QRect(350, 0, 30, 30))

        self.work_reserve_checkbox = QCheckBox(window)
        self.work_reserve_checkbox.setGeometry(QRect(385, 6, 20, 20))
        self.work_reserve_label = QLabel(window)
        self.work_reserve_label.setText("비축")
        self.work_reserve_label.setGeometry(QRect(405, 0, 30, 30))

        self.work_etc_checkbox = QCheckBox(window)
        self.work_etc_checkbox.setGeometry(QRect(440, 6, 20, 20))
        self.work_etc_label = QLabel(window)
        self.work_etc_label.setText("기타")
        self.work_etc_label.setGeometry(QRect(460, 0, 30, 30))

        self.work_private_checkbox = QCheckBox(window)
        self.work_private_checkbox.setGeometry(QRect(495, 6, 20, 20))
        self.work_private_label = QLabel(window)
        self.work_private_label.setText("민간")
        self.work_private_label.setGeometry(QRect(515, 0, 30, 30))
        self.work_private_checkbox.setChecked(True)

        #공고명
        self.announcement_name_label = QLabel(window)
        self.announcement_name_label.setText("공고명")
        self.announcement_name_label.setGeometry(QRect(10, 30, 40, 30))

        self.announcement_name_line = QLineEdit(window)
        self.announcement_name_line.setGeometry(QRect(70, 30, 400, 30))
        
        # 공고/개찰일
        self.deadline_label = QLabel(window)
        self.deadline_label.setText("공고/개찰일")
        self.deadline_label.setGeometry(QRect(10, 60, 70, 30))

        self.deadline_1month_checkbox = QRadioButton(window)
        self.deadline_1month_checkbox.setGeometry(QRect(110, 66, 20, 20))
        self.deadline_1month_label = QLabel(window)
        self.deadline_1month_label.setText("최근1개월")
        self.deadline_1month_label.setGeometry(QRect(130, 60, 60, 30))
        self.deadline_1month_checkbox.setChecked(True)

        self.deadline_3month_checkbox = QRadioButton(window)
        self.deadline_3month_checkbox.setGeometry(QRect(195, 66, 20, 20))
        self.deadline_3month_label = QLabel(window)
        self.deadline_3month_label.setText("최근3개월")
        self.deadline_3month_label.setGeometry(QRect(215, 60, 60, 30))

        self.deadline_6month_checkbox = QRadioButton(window)
        self.deadline_6month_checkbox.setGeometry(QRect(280, 66, 20, 20))
        self.deadline_6month_label = QLabel(window)
        self.deadline_6month_label.setText("최근6개월")
        self.deadline_6month_label.setGeometry(QRect(300, 60, 60, 30))

        # 기관명
        self.organization_label = QLabel(window)
        self.organization_label.setText("기관명")
        self.organization_label.setGeometry(QRect(10, 90, 40, 30))

        self.organization_line = QLineEdit(window)
        self.organization_line.setGeometry(QRect(70, 90, 200, 30))

        # 실행
        self.execute_button = QPushButton(window)
        self.execute_button.setText("검색")
        self.execute_button.setGeometry(QRect(450, 90, 100, 30))

    