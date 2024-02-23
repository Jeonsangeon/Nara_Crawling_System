from main_system.main_system_ui import MainSystemUi
from auto_system.auto_system import webCrawling
from auto_system.write_data import make_excel
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import *

class MainSystem(QMainWindow, MainSystemUi):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.work_all_checkbox.clicked.connect(self.when_all_checkbox_clicked)
        self.work_article_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_construction_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_service_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_lease_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_foreign_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_reserve_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_etc_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_private_checkbox.clicked.connect(self.when_other_checkbox_clicked)

        self.execute_button.clicked.connect(self.run)

    def when_all_checkbox_clicked(self):
        self.work_article_checkbox.setChecked(False)
        self.work_construction_checkbox.setChecked(False)
        self.work_service_checkbox.setChecked(False)
        self.work_lease_checkbox.setChecked(False)
        self.work_foreign_checkbox.setChecked(False)
        self.work_reserve_checkbox.setChecked(False)
        self.work_etc_checkbox.setChecked(False)
        self.work_private_checkbox.setChecked(False)
    
    def when_other_checkbox_clicked(self):
        self.work_all_checkbox.setChecked(False)

    def run(self):
        work_list = []
        if self.work_all_checkbox.isChecked():
            work_list.append("")
        else:
            if self.work_article_checkbox.isChecked():
                work_list.append(1)
            if self.work_construction_checkbox.isChecked():
                work_list.append(3)
            if self.work_service_checkbox.isChecked():
                work_list.append(5)
            if self.work_lease_checkbox.isChecked():
                work_list.append(6)
            if self.work_foreign_checkbox.isChecked():
                work_list.append(2)
            if self.work_reserve_checkbox.isChecked():
                work_list.append(11)
            if self.work_etc_checkbox.isChecked():
                work_list.append(4)
            if self.work_private_checkbox.isChecked():
                work_list.append(20)
        if self.deadline_1month_checkbox.isChecked():
            deadline = 1
        elif self.deadline_3month_checkbox.isChecked():
            deadline = 2
        else:
            deadline = 3
        option = [work_list, self.announcement_name_line.text(), deadline, self.organization_line.text()]
        announce_list = webCrawling(work_list, self.announcement_name_line.text(), deadline, self.organization_line.text())
        make_excel(announce_list, option)

        QMessageBox.about(self, "입찰공고 목록 작성완료", f"작성 결과: 총 {len(announce_list)} 항목이 작성되었습니다.")