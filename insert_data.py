
import sqlite3
from XBRLParser import *





def insert_annual_report_data_and_data_data(root):
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    sqle= 'SELECT companies_id, published_date FROM annual_reports'
    existing_annual_reports = c.execute(sqle).fetchall()

    where1 = (getEdinetCode(root),)
    print(where1)
    sql1 = 'SELECT id FROM companies WHERE edinet_code=?'
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
        insert_data_data(root, companies_id)

    if data_tuple in existing_annual_reports:
        print(u'同じxbrlファイルを検知しました。スキップします。')



def insert_data_data(root, company_id):
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    where1 = (company_id, getPublishDate(root))
    sql1 = 'SELECT id FROM annual_reports WHERE companies_id=? AND published_date=?'
    annual_report_id= c.execute(sql1, where1).fetchall()[0][0]
    print(where1[1])

    where2 = (company_id,)
    sqlwow = 'SELECT consolidated FROM companies WHERE id= ?'

    company_consolidated = c.execute(sqlwow, where2).fetchall()[0][0]

    sql2 = 'SELECT id, parameter_name FROM parameters'
    parameters_data = c.execute(sql2).fetchall()

    data_data = []

    if company_consolidated == 0:
        for each in parameters_data:
            value = getValue(each[1], root, False)
            if value != None:
                data_data.append((annual_report_id, each[0], value, 0))
    else:
        for each in parameters_data:
            value1 = getValue(each[1], root, False)
            if value1 != None:
                data_data.append((annual_report_id, each[0], value1, 0))

            value2 = getValue(each[1], root, True)
            if value2 != None:
                data_data.append((annual_report_id, each[0], value2, 1))


    for each in data_data:
        sql4 = 'INSERT INTO data VALUES(NULL, ?, ?, ?, ?)'
        c.execute(sql4, each)

    conn.commit()
    conn.close()

