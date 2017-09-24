import glob

import xlrd


def getEdinetCodeFromExcelFile(file_name,shouken_code):
    list=[]
    for name in glob.iglob(file_name+'.xlsx'):
        book = xlrd.open_workbook(name)
        sheet1 = book.sheet_by_index(0)
        for cellNum in range(sheet1.nrows):
            list.append(sheet1.cell(cellNum,0).value)
    return list

def getShoukenCodeFromExcelFile(file_name):
    list=[]
    for name in glob.iglob(file_name+'.xlsx'):
        book = xlrd.open_workbook(name)
        sheet1 = book.sheet_by_index(0)
        for cellNum in range(sheet1.nrows):
            list.append(sheet1.cell(cellNum,11).value)
    return list


shoken_codes = getEdinetCodeFromExcelFile("syouken_code")
edinet_codes = getShoukenCodeFromExcelFile("EdinetcodeDlInfo")



print(shoken_codes)
print(edinet_codes)


