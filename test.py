import glob
from lxml import etree
from xml.dom import minidom
from datase_schema import set_up_database
from insert_data import insert_annual_report_data_and_data_data
import datetime
import os.path


XBRL_FILES_URL="xbrls/"

if  os.path.isfile(".\\xlrd_data.db") is False:
    set_up_database()
else:
    print('データベースがすでに存在します')

files = glob.glob(XBRL_FILES_URL + '*xbrl')
for file in files:
    dom = minidom.parse(file)
    root = etree.fromstring(dom.toxml())

    insert_annual_report_data_and_data_data(root)

