
import sqlite3
from XBRLParser import *





def insert_annual_report_data(root):
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    sqle= 'SELECT companies_id, published_date FROM annual_reports'
    existing_annual_reports = c.execute(sqle).fetchall()

    where1 = (getCompanyName(root),)
    print(where1)
    sql1 = 'SELECT id FROM companies WHERE company_name_kanji=?'
    companies_id = c.execute(sql1, where1).fetchall()[0][0]

    conn.commit()
    conn.close()

    sql2 = 'INSERT INTO annual_reports VALUES(NULL, ?, ?)'
    data_tuple = (companies_id, getPublishDate(root))

    if data_tuple not in existing_annual_reports:
        conn = sqlite3.connect('xlrd_data.db')
        c = conn.cursor()

        c.execute(sql2, data_tuple)

        conn.commit()
        conn.close()
        return 0
    if data_tuple in existing_annual_reports:
        return 1

def insert_data_data(root, isConsolidated):
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()


    where1 = (getPublishDate(root),)
    print(where1)
    sql1 = 'SELECT id FROM annual_reports WHERE published_date=?'
    annual_report_id = c.execute(sql1, where1).fetchall()[0][0]

    sql2 = 'SELECT id, parameter_name FROM parameters'
    parameters_data = c.execute(sql2).fetchall()

    data_data = []

    counter = 0
    for each in parameters_data:
        value = getValue(each[1], root, isConsolidated)
        if value != None:
            data_data.append((annual_report_id, each[0], value))
            counter += 1
            delimitter = len(parameters_data) / 10
            if counter == delimitter:
                counter = 0
                print("#", end='')
    print()



    for each in data_data:
        sql4 = 'INSERT INTO data VALUES(NULL, ?, ?, ?)'
        c.execute(sql4, each)

    conn.commit()
    conn.close()


def insert_data(root, isConsolidated):

    if insert_annual_report_data(root) == 0:
        insert_data_data(root, isConsolidated)
    else:
        print(u'同じxbrlファイルを検知しました。スキップします。')
