import urllib.request
from xml.dom import minidom
from lxml import etree as ElementTree
import re
import xlrd
import glob

UFO_CATCHER_PATH="http://resource.ufocatch.com/atom/edinetx/query/"
XBRL_FILES_DIRECTORY='./xbrls/'

def getXBRL_UrlOfFirm(edinetCode):

    dom = minidom.parse(urllib.request.urlopen(UFO_CATCHER_PATH+str(edinetCode)))
    root = ElementTree.fromstring(dom.toxml())
    link_list={}

    XPATH_HEAD = "{"+root.xpath("namespace-uri(.)")+"}"

    for entry in root.findall(XPATH_HEAD+'entry'):
        text=entry.find(XPATH_HEAD+'title').text
        matchObj=re.search(r"^(?!.*訂正).*(?=有価証券報告書).*$",text)
        if(matchObj):
            for link in entry.findall(XPATH_HEAD+'link'):
                link_text=link.get("href")
                xbrl_link_text= re.search(r"^(?!.*AuditDoc).*xbrl$",link_text)

                if(xbrl_link_text):
                    link_list.update({text:link_text})
    return link_list


def downLoadFile(list):
    for url_key in list.keys():
        urllib.request.urlretrieve(list[url_key], XBRL_FILES_DIRECTORY+url_key+".xbrl")
        print("download complete: "+url_key)


def getEdinetCodeFromExcelFile():
    list=[]
    for name in glob.iglob('*.xlsx'):
        book=xlrd.open_workbook(name)
        sheet1 = book.sheet_by_index(0)
        for cellNum in range(sheet1.nrows):
            list.append(sheet1.cell(cellNum,0).value)
    return list





for edinetCode in getEdinetCodeFromExcelFile():
    downLoadFile(getXBRL_UrlOfFirm(edinetCode))
