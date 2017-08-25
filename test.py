import glob
from lxml import etree
from xml.dom import minidom
from datase_schema import set_up_database
from insert_data import insert_annual_report_data_and_data_data
import datetime
import os.path


XBRL_FILES_URL="xbrls/"

if  os.path.exists("\\xlrd_data.db"):
    set_up_database()

# conn = sqlite3.connect('xlrd_data.db')
# c = conn.cursor()
#
# hatena = ('jppfs_cor',)
# sql = 'SELECT prefix FROM parameters WHERE prefix != ?'
# data = c.execute(sql, hatena).fetchall()
# print(data)



files = glob.glob(XBRL_FILES_URL + '*xbrl')
for file in files:
    dom = minidom.parse(file)
    root = etree.fromstring(dom.toxml())

    insert_annual_report_data_and_data_data(root)

