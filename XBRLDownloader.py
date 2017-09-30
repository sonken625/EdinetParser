import urllib.request
from xml.dom import minidom
from lxml import etree as ElementTree
import re
import xlrd
import glob

UFO_CATCHER_PATH="http://resource.ufocatch.com/atom/edinetx/query/"
XBRL_FILES_DIRECTORY='./xbrls/'
PDF_DIRECTORY="./pdfs/"

def getXBRL_UrlOfFirm(edinetCode):

    dom = minidom.parse(urllib.request.urlopen(UFO_CATCHER_PATH+str(edinetCode)))
    root = ElementTree.fromstring(dom.toxml())
    link_list={}

    XPATH_HEAD = "{"+root.xpath("namespace-uri(.)")+"}"

    for entry in root.findall(XPATH_HEAD+'entry'):
        text=entry.find(XPATH_HEAD+'title').text
        matchObj=re.search(r"^(?!.*訂正).*(?=有価証券届出書（新規公開時）).*$",text)
        if(matchObj):
            for link in entry.findall(XPATH_HEAD+'link'):
                link_text=link.get("href")
                xbrl_link_text= re.search(r"^(?!.*AuditDoc).*xbrl$",link_text)

                if(xbrl_link_text):
                    link_list.update({text:link_text})
        else:
            print("有価証券届出書（新規公開時）はありません")
    return link_list

def get_pdf_url(edinet_code):
    dom = minidom.parse(urllib.request.urlopen(UFO_CATCHER_PATH + str(edinet_code)))
    root = ElementTree.fromstring(dom.toxml())
    link_list = {}

    XPATH_HEAD = "{" + root.xpath("namespace-uri(.)") + "}"

    for entry in root.findall(XPATH_HEAD + 'entry'):
        text = entry.find(XPATH_HEAD + 'title').text
        matchObj = re.search(r"^(?!.*訂正).*(?=有価証券届出書（新規公開時）).*$", text)
        if (matchObj):
            link_text= [link_text for link_text in entry.findall(XPATH_HEAD+'link') if link_text.get("type")=="application/pdf"]
            if(len(link_text)!=0 and link_text[0].get("href")):
                print(link_text[0])
                link_list.update({text: link_text[0].get("href")})

        else:
            print("有価証券届出書（新規公開時）はありません")

    return link_list


def downLoadFile(list):
    for url_key in list.keys():
        print(list[url_key])
        urllib.request.urlretrieve(list[url_key], XBRL_FILES_DIRECTORY+url_key+".xbrl")
        print("download complete: "+url_key)


def getEdinetCodeFromExcelFile(file_name):
    list=[]
    for name in glob.iglob(file_name+'.xlsx'):
        book = xlrd.open_workbook(name)
        sheet1 = book.sheet_by_index(0)
        for cellNum in range(sheet1.nrows):
            list.append(sheet1.cell(cellNum,0).value)
    return list


# for edinetCode in getEdinetCodeFromExcelFile():
#     downLoadFile(getXBRL_UrlOfFirm(edinetCode))

for edinet_code in getEdinetCodeFromExcelFile("forTest"):
    print(edinet_code)
    downLoadFile(getXBRL_UrlOfFirm(edinet_code))
