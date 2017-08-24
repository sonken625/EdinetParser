import glob
from lxml import etree
from xml.dom import minidom
from datase_schema import set_up_database
from insert_data import insert_all_data
import sqlite3


XBRL_FILES_URL="xbrls/"



set_up_database()

# conn = sqlite3.connect('xlrd_data.db')
# c = conn.cursor()
#
# hatena = ('jppfs_cor',)
# sql = 'SELECT prefix FROM parameters WHERE prefix != ?'
# data = c.execute(sql, hatena).fetchall()
# print(data)



files = glob.glob(XBRL_FILES_URL + '*.xbrl')
for file in files:
    dom = minidom.parse(file)
    root = etree.fromstring(dom.toxml())

    insert_all_data(root)
