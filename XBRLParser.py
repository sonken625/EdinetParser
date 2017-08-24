from xml.dom import minidom
import glob
from lxml import etree

CONSOLIDATED_TEXT="CurrentYearConsolidatedInstant"
REBASED_CONSOLIDATED_TEXT="CurrentYearInstant"
NON_CONSOLIDATED_TEXT="CurrentYearNonConsolidatedInstant"
REBASED_NON_CONSOLIDATED_TEXT="CurrentYearInstant_NonConsolidatedMember"







#rootにはetreeオブジェクトを入れる
#一回パースしてから実行したほうが早いから
# (例) dom = minidom.parse(fileUrl)
#      root = etree.fromstring(dom.toxml())
def getValue(tagName,root,isConsolidated):
    nameSpaces = root.nsmap

    for nameSpace in nameSpaces:
        elements = root.findall(nameSpace+":"+tagName, nameSpaces)
        if(len(elements)==0):
            continue
        if (isConsolidated==True):
            for element in elements:
                if (element.get("contextRef") == CONSOLIDATED_TEXT or element.get("contextRef") == REBASED_CONSOLIDATED_TEXT):
                    return element.text
        else:
            for element in elements:
                if (element.get("contextRef") == NON_CONSOLIDATED_TEXT or element.get("contextRef") == REBASED_NON_CONSOLIDATED_TEXT):
                    return element.text


#rootにはetreeオブジェクトを入れる
#一回パースしてから実行したほうが早いから
# (例) dom = minidom.parse(fileUrl)
#      root = etree.fromstring(dom.toxml())

def getPublishDate(root):
    nameSpaces = root.nsmap
    elements = root.findall("xbrli:context", nameSpaces)
    for element in elements:
        if(element.get("id")==NON_CONSOLIDATED_TEXT or element.get("id")==REBASED_NON_CONSOLIDATED_TEXT):
            return element.find(".//xbrli:instant",nameSpaces).text


#rootにはetreeオブジェクトを入れる
#一回パースしてから実行したほうが早いから
# (例) dom = minidom.parse(fileUrl)
#      root = etree.fromstring(dom.toxml())
def getCompanyName(root):
    nameSpaces = root.nsmap
    if("jpfr-di" in nameSpaces):
        return root.find("jpfr-di:EntityNameJaEntityInformation", nameSpaces).text
    elif("jpcrp_cor" in nameSpaces):
        return root.find("jpcrp_cor:CompanyNameCoverPage", nameSpaces).text



def getEdinetCode(root):
    nameSpaces = root.nsmap
    return root.find(".//xbrli:identifier",nameSpaces).text[0:6]




#XBRL_FILES_URL="xbrls/"
# files = glob.glob(XBRL_FILES_URL + '*.xbrl')
# dom = minidom.parse(files[0])
# root = etree.fromstring(dom.toxml())
# print(getEdinetCode(root))

#XBRL_FILES_URL="xbrls/"
# def getData(tagName,isConsolidated):
#     files = glob.glob(XBRL_FILES_URL + '*.xbrl')
#     for file in files:
#        print(getCompanyName(file))