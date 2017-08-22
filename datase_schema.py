import unicodedata
import xlrd
import sqlite3
import re

COLUMN_NAME_DATA_URL="ColumnNameData/"


sql_dict = {'companys' : 'id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, business_category INTEGER', 'annual_reports':'id INTEGER PRIMARY KEY AUTOINCREMENT, company_id INTEGER, published_date TEXT',
'data': 'id INTEGER PRIMARY KEY AUTOINCREMENT, annual_report_id INTEGER, parameter_id INTEGER, data TEXT', 'parameters' : 'id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, sheet_type_id INTEGER',
'sheet_types' :'id INTEGER PRIMARY KEY AUTOINCREMENT, sheet_name TEXT', 'company_category': 'id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT'}


conn=sqlite3.connect('xlrd_data.db')
c = conn.cursor()

for k,v in sql_dict.items():
    sql = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (k, v)
    c.execute(sql)

conn.commit()
conn.close()


def is_not_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return False
    return True


file = xlrd.open_workbook(COLUMN_NAME_DATA_URL+'1f.xls')



#パラメタテーブル
param_data = []

for names in file.sheet_names():


    if(re.match(u"目次",names) ==None and re.match(u"勘定科目リストについて",names)==None):
        print(names)
        sheet = file.sheet_by_name(names)

        significant = False
        bs = False
        pl = False
        cf = False

        for row in range(0, sheet.nrows):

            variable_name = sheet.cell(row, 8).value
            type = sheet.cell(row, 9).value
            first_column = sheet.cell(row, 0).value
            second_column = sheet.cell(row, 1).value
            abstract = sheet.cell(row, 13).value

            if first_column != '' and second_column == '':
                if re.match(u"貸借対照表*", first_column) != None:
                    significant = True
                    bs = True
                    pl = False
                    cf = False
                elif re.match(u"損益計算書*", first_column) != None:
                    significant = True
                    bs = False
                    pl = True
                    cf = False
                elif re.match(u"キャッシュ・フロー計算書*", first_column) != None:
                    significant = True
                    bs = False
                    pl = False
                    cf = True
                else:
                    significant = False
                    bs = False
                    pl = False
                    cf = True
            if significant == True:
                if is_not_japanese(variable_name) and variable_name != '' and type != 'substitutionGroup':
                    if bs == True and [variable_name, type] not in param_data and abstract == 'false':
                        param_data.append((variable_name, type, 1))
                    if pl == True and [variable_name, type] not in param_data and abstract == 'false':
                        param_data.append((variable_name, type, 2))
                    if cf == True and [variable_name, type] not in param_data and abstract == 'false':
                        param_data.append((variable_name, type, 3))



conn = sqlite3.connect('xlrd_data.db')
c = conn.cursor()

sql = 'INSERT INTO parameters VALUES (NULL, ?, ?, ?)'
for each in param_data:
    c.execute(sql, each)

conn.commit()
conn.close()



# sheet table
conn = sqlite3.connect('xlrd_data.db')
c = conn.cursor()

insert = [('bs',), ('pl',), ('cf',)]

for each in insert:
    sql = 'INSERT INTO sheet_types VALUES( NULL, ?)'
    c.execute(sql, tuple(each))
conn.commit()
conn.close()

