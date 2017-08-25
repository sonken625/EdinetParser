import glob
from lxml import etree
from xml.dom import minidom
from datase_schema import set_up_database
from insert_data import insert_annual_report_data_and_data_data
import time
import os.path



XBRL_FILES_URL="xbrls/"

if  os.path.isfile(".\\xlrd_data.db") is False:
    print('データベース作成中')
    set_up_database()
    print('データベース作成完了')
else:
    print('データベースがすでに存在します')

files = glob.glob(XBRL_FILES_URL + '*xbrl')
for file in files:
    start = time.time()

    dom = minidom.parse(file)
    root = etree.fromstring(dom.toxml())
    io_time = time.time()-start

    insert_annual_report_data_and_data_data(root)
    per_xbrl_execution_time = time.time() - start

    print('io time = %s' % io_time)
    print ("per xbrl time = %s" % per_xbrl_execution_time)

