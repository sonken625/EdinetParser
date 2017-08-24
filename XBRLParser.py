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



#TagNameは検索する財務諸表項目名。isConsolidatedは連結情報をとるのかどうか。trueだと連結された情報のみをとる
def getValue(tagName,root,isConsolidated):
    nameSpaces = root.nsmap

    #jpfr-t-cteというnamespaceがあれば古い規格
    #古い規格の場合jpfr-tから始まるnamespace全てで検索
    #新しい場合はjppfs_corというnamespaceのみで検索
    if "jpfr-t-cte" in nameSpaces.keys():
        for nameSpace in nameSpaces:
            if (nameSpace.startswith("jpfr-t-")):
                elements = root.findall(nameSpace + ":" + tagName, nameSpaces)

                if (elements != None and len(elements) != 0):
                    return getCurrentYearDateFromSearchedElements(elements, isConsolidated)
    else:
        elements = root.findall("jppfs_cor:" + tagName, nameSpaces)
        if (elements != None and len(elements) != 0):
           return getCurrentYearDateFromSearchedElements(elements, isConsolidated)


def getCurrentYearDateFromSearchedElements(elements, isConsolidated):
        for element in elements:
            if (isConsolidated == True):
                if (element.get("contextRef") == CONSOLIDATED_TEXT or element.get(
                        "contextRef") == REBASED_CONSOLIDATED_TEXT):
                    return element.text
            else:
                if (element.get("contextRef") == NON_CONSOLIDATED_TEXT or element.get(
                        "contextRef") == REBASED_NON_CONSOLIDATED_TEXT):
                    return element.text



def getPublishDate(root):
    nameSpaces = root.nsmap
    elements = root.findall("xbrli:context", nameSpaces)
    for element in elements:
        if(element.get("id")==NON_CONSOLIDATED_TEXT or element.get("id")==REBASED_NON_CONSOLIDATED_TEXT):
            return element.find(".//xbrli:instant",nameSpaces).text


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
# def getData(tagName,isConsolidated):
#     files = glob.glob(XBRL_FILES_URL + '*.xbrl')
#     for file in files:
#        print(getCompanyName(file))