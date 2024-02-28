from pre_standard.pre_standard_ui import PreStandardUi
from PySide6.QtWidgets import *
from auto_system.write_data import init_excel
from auto_system.auto_system import pre_standard_crawling

class PreStandard(QDialog, PreStandardUi):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.work_all_checkbox.clicked.connect(self.when_all_checkbox_clicked)
        self.work_article_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_construction_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_service_checkbox.clicked.connect(self.when_other_checkbox_clicked)
        self.work_foreign_checkbox.clicked.connect(self.when_other_checkbox_clicked)

        self.execute_button.clicked.connect(self.run)

    def when_other_checkbox_clicked(self):
        self.work_all_checkbox.setChecked(False)

    def when_all_checkbox_clicked(self):
        self.work_article_checkbox.setChecked(False)
        self.work_construction_checkbox.setChecked(False)
        self.work_service_checkbox.setChecked(False)
        self.work_foreign_checkbox.setChecked(False)

    def run(self):
        work_list = []
        if self.work_all_checkbox.isChecked():
            work_list.append("A")
        else:
            if self.work_article_checkbox.isChecked():
                work_list.append(1)
            if self.work_construction_checkbox.isChecked():
                work_list.append(3)
            if self.work_service_checkbox.isChecked():
                work_list.append(5)
            if self.work_foreign_checkbox.isChecked():
                work_list.append(2)
        option = [self.agency_line.text(), work_list, self.business_name_line.text()]
        init_excel(option, notice=False)
        pre_standard_crawling(option[0], option[1], option[2])
        self.agency_line.clear()
        self.business_name_line.clear()