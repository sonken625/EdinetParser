import codecs
import unicodedata
import xlrd
import sqlite3
import re
import pandas as pd

COLUMN_NAME_DATA_URL="ColumnNameData/"
EDINET_CODE_NAME_DATA_URL="ALLEdinetCode/"




def create_tables():
    sql_dict = {'business_categories': 'id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT',
                'company_types'      : 'id INTEGER PRIMARY KEY AUTOINCREMENT, company_type_name',
                'companies'          : 'id INTEGER PRIMARY KEY AUTOINCREMENT, business_categories_id, company_types_id, company_name_kanji TEXT,'
                                       ' company_name_alphabet TEXT, company_name_katakana TEXT, edinet_code TEXT, listed INTEGER, consolidated INTEGER,'
                                       ' capital INTEGER, settling_date TEXT, address TEXT, code INTEGER',
                'annual_reports'     : 'id INTEGER PRIMARY KEY AUTOINCREMENT, companies_id INTEGER, published_date TEXT',
                'data'               : 'id INTEGER PRIMARY KEY AUTOINCREMENT, annual_reports_id INTEGER, parameters_id INTEGER, data TEXT',
                'parameters'         : 'id INTEGER PRIMARY KEY AUTOINCREMENT, sheet_types_id INTEGER, parameter_name TEXT, type TEXT',
                'sheet_types'        : 'id INTEGER PRIMARY KEY AUTOINCREMENT, sheet_name TEXT'}

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



def set_up_parameters_table():
    file = xlrd.open_workbook(COLUMN_NAME_DATA_URL+'1f.xls')

    param_data = []

    for names in file.sheet_names():


        if(re.match(u"目次",names) ==None and re.match(u"勘定科目リストについて",names)==None):
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
                            param_data.append((1, variable_name, type))
                        if pl == True and [variable_name, type] not in param_data and abstract == 'false':
                            param_data.append((2, variable_name, type))
                        if cf == True and [variable_name, type] not in param_data and abstract == 'false':
                            param_data.append((3, variable_name, type))



    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    sql = 'INSERT INTO parameters VALUES (NULL, ?, ?, ?)'
    for each in param_data:
        c.execute(sql, each)

    conn.commit()
    conn.close()



def set_up_sheet_types_table():
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    insert = [('bs',), ('pl',), ('cf',)]

    for each in insert:
        sql = 'INSERT INTO sheet_types VALUES( NULL, ?)'
        c.execute(sql, tuple(each))
    conn.commit()
    conn.close()




def set_up_business_categories_table():
    with codecs.open(EDINET_CODE_NAME_DATA_URL+'EdinetcodeDlInfo.csv', "r", "Shift-JIS", "ignore") as file:
        df = pd.read_table(file, delimiter=",", skiprows=2, header=None)
    list = df[10].values.tolist()

    list_uniq = []
    for x in list:
        if x not in list_uniq and re.search(u'個人', x) is None and re.search(u'政府', x) is None:
            list_uniq.append(x)
    tuple_uniq = tuple(list_uniq)

    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    for each in tuple_uniq:
        sql = 'INSERT INTO business_categories VALUES(NULL, ?)'

        c.execute(sql, (each,))
    conn.commit()
    conn.close()




def set_up_company_types_table():
    with codecs.open(EDINET_CODE_NAME_DATA_URL+'EdinetcodeDlInfo.csv', "r", "Shift-JIS", "ignore") as file:
        df = pd.read_table(file, delimiter=",", skiprows=2, header=None)
    list = df[1].values.tolist()

    list_uniq = []
    for x in list:
        if x not in list_uniq and re.search(u'個人', x) is None and re.search(u'政府', x) is None:
            list_uniq.append(x)
    tuple_uniq = tuple(list_uniq)

    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    for each in tuple_uniq:
        sql = 'INSERT INTO company_types VALUES(NULL, ?)'

        c.execute(sql, (each,))
    conn.commit()
    conn.close()


# id, cat_id, type_id, name6, alphabet7, kana8, edinetcode0, listed2, consolidated3, capital4, date5, add9, code11, cat10, type1
def set_up_companies_table():
    with codecs.open(EDINET_CODE_NAME_DATA_URL+'EdinetcodeDlInfo.csv', "r", "Shift-JIS", "ignore") as file:
        df = pd.read_table(file, delimiter=",", skiprows=2, header=None)
    df = df.iloc[:, [6, 7, 8, 0, 2, 3, 4, 5, 9, 11, 10, 1]]
    df = df[df[10].str.contains("個人")==False]
    df = df[df[1].str.contains("政府")==False]

    parsed_list = df.values.tolist()

    list = []
    for each in parsed_list:
        insert_list = []
        for x in each:
            if x == u'上場' or x == u'有':
                insert_list.append(1)
            elif x == u'非上場' or x == u'無':
                insert_list.append(0)
            else:
                insert_list.append(x)
        list.append(insert_list)


    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()


    for each in list:
        if  re.search(u'個人', each[10]) is None and re.search(u'政府', each[10]) is None:
            select_data = each[10]
            sql1 = 'SELECT id FROM business_categories WHERE category_name = ?'
            cat_id = c.execute(sql1, (select_data,)).fetchall()[0][0]

        if  re.search(u'個人', each[11]) is None and re.search(u'政府', each[11]) is None:
            select_data2 = each[11]
            sql2 = 'SELECT id FROM company_types WHERE company_type_name = ?'
            type_id = c.execute(sql2, (select_data2,)).fetchall()[0][0]

        insert_tuple = (cat_id, type_id, each[0], each[1], each[2], each[3],each[4],each[5],each[6],each[7],each[8],each[9])
        sql3 = 'INSERT INTO companies VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(sql3, insert_tuple)

    conn.commit()
    conn.close()


def set_up_database():
    create_tables()
    set_up_sheet_types_table()
    set_up_parameters_table()
    set_up_business_categories_table()
    set_up_company_types_table()
    set_up_companies_table()
