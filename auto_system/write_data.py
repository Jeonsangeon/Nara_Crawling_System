import openpyxl

def make_excel(announce_list, option):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = '공고목록'
    worksheet.append(['업무', '공고번호-차수', '분류', '공고명', '공고기관', '수요기관', '계약방법', '입력일시(입찰마감일시)', '공동수급'])

    for row in announce_list:
        worksheet.append(row)
    
    worksheet = workbook.create_sheet('설정옵션')
    worksheet.append(['업무', '공고명', '공고/개찰일', '기관명'])

    for index, value in enumerate(option[0], 2):
        if not value:
            worksheet[f'A{index}'] = "전체"
        else:
            if value == 1:
                worksheet[f'A{index}'] = "물품"
            if value == 3:
                worksheet[f'A{index}'] = "공사"
            if value == 5:
                worksheet[f'A{index}'] = "용역"
            if value == 6:
                worksheet[f'A{index}'] = "리스"
            if value == 2:
                worksheet[f'A{index}'] = "외자"
            if value == 11:
                worksheet[f'A{index}'] = "비축"
            if value == 4:
                worksheet[f'A{index}'] = "기타"
            if value == 20:
                worksheet[f'A{index}'] = "민간"
    worksheet['B2'] = option[1]
    if option[2] == 1:
        worksheet['C2'] = '최근1개월'
    elif option[2] == 2:
        worksheet['C2'] = '최근3개월'
    else:
        worksheet['C2'] = '최근6개월'
    worksheet['D2'] = option[3]

    workbook.save(filename='입찰공고목록.xlsx')