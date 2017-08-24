import glob

from lxml import etree
from xml.dom import minidom

from datase_schema import set_up_database
from insert_data import insert_data


XBRL_FILES_URL="xbrls/"



set_up_database()
files = glob.glob(XBRL_FILES_URL + '*.xbrl')
for file in files:
    dom = minidom.parse(file)
    root = etree.fromstring(dom.toxml())

    insert_data(root, False)
