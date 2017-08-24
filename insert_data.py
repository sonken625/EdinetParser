
import sqlite3
from XBRLParser import *




fileUrl='xbrls2/縲職00040縲鷹未譚ｱ螟ｩ辟ｶ逑ｦ譁ｯ髢狗匱譬ｪ蠑丈ｼ夂､ｾ 譛我ｾ｡險ｼ蛻ｸ蝣ｱ蜻頑嶌 窶・隨ｬ149譛滂ｼ亥ｹｳ謌・2蟷ｴ1譛・譌･ 窶・蟷ｳ謌・2蟷ｴ12譛・1譌･・・xbrl'
dom = minidom.parse(fileUrl)
root = etree.fromstring(dom.toxml())

def insert_annual_report_data(root):
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    where1 = (getCompanyName(root),)
    sql1 = 'SELECT id FROM companies WHERE company_name_kanji=?'
    companies_id = c.execute(sql1, where1).fetchall()[0][0]

    sql2 = 'INSERT INTO annual_reports VALUES(NULL, ?, ?)'
    data_tuple = (companies_id, getPublishDate(root))

    c.execute(sql2, data_tuple)

    conn.commit()
    conn.close()

def insert_data_data(root, isConsolidated):
    conn = sqlite3.connect('xlrd_data.db')
    c = conn.cursor()

    where1 = (getPublishDate(root),)
    sql1 = 'SELECT id FROM annual_reports WHERE published_date=?'
    annual_report_id = c.execute(sql1, where1).fetchall()[0][0]

    sql2 = 'SELECT id, parameter_name FROM parameters'
    parameters_data = c.execute(sql2).fetchall()

    data_data = []

    for each in parameters_data:
        data_data.append((annual_report_id, each[0], getValue(each[1], root, isConsolidated)))

    for each in data_data:
        sql4 = 'INSERT INTO data VALUES(NULL, ?, ?, ?)'
        c.execute(sql4, each)
        print('appended data')


def insert_data(root, isConsolidated):

    insert_annual_report_data(root)
    insert_data_data(root, isConsolidated)

insert_data(root, False)
