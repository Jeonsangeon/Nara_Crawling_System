from pre_standard.pre_standard_ui import PreStandardUi
from PySide6.QtWidgets import *
from auto_system.write_data import init_excel, make_prestandard_sheet
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
        agency_option = []
        if self.demand_agency_button.isChecked():
            agency_option.append(2)
        else:
            agency_option.append(1)
        agency_option.append(self.agency_line.text())
        work_option = []
        if self.work_all_checkbox.isChecked():
            work_option.append("A")
        else:
            if self.work_article_checkbox.isChecked():
                work_option.append(1)
            if self.work_construction_checkbox.isChecked():
                work_option.append(3)
            if self.work_service_checkbox.isChecked():
                work_option.append(5)
            if self.work_foreign_checkbox.isChecked():
                work_option.append(2)
        option = [agency_option, work_option, self.business_name_line.text()]
        init_excel(option, notice=False)
        input_data = pre_standard_crawling(option[0], option[1], option[2])
        make_prestandard_sheet(input_data)
        self.agency_line.clear()
        self.business_name_line.clear()
        QMessageBox.about(self, "사전규격 목록 작성완료", f"작성 결과: 총 {len(input_data)}개 데이터가 작성되었습니다.")