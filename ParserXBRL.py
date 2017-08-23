from xml.dom import minidom
import glob
from lxml import etree

CONSOLIDATED_TEXT="CurrentYearConsolidatedInstant"
REBASED_CONSOLIDATED_TEXT="CurrentYearInstant"
NON_CONSOLIDATED_TEXT="CurrentYearNonConsolidatedInstant"
REBASED_NON_CONSOLIDATED_TEXT="CurrentYearInstant_NonConsolidatedMember"

#write directory where xbrl files are
XBRL_FILES_URL="xbrls/"


def getValue(tagName,fileUrl,isConsolidated):
    root = __createEtreeObjectFromFileURL(fileUrl)

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


def getPublishDate(fileUrl):
    root = __createEtreeObjectFromFileURL(fileUrl)

    nameSpaces = root.nsmap
    elements = root.findall("xbrli:context", nameSpaces)
    for element in elements:
        if(element.get("id")==NON_CONSOLIDATED_TEXT or element.get("id")==REBASED_NON_CONSOLIDATED_TEXT):
            return element.find(".//xbrli:instant",nameSpaces).text


def getCompanyName(fileUrl):
    root = __createEtreeObjectFromFileURL(fileUrl)

    nameSpaces = root.nsmap
    if("jpfr-di" in nameSpaces):
        return root.find("jpfr-di:EntityNameJaEntityInformation", nameSpaces).text
    elif("jpcrp_cor" in nameSpaces):
        return root.find("jpcrp_cor:CompanyNameCoverPage", nameSpaces).text

def __createEtreeObjectFromFileURL(fileUrl):
    dom = minidom.parse(fileUrl)
    root = etree.fromstring(dom.toxml())
    return root



#
# files = glob.glob(XBRL_FILES_URL + '*.xbrl')
# print(getCompanyName(files[0]))


#
# def getData(tagName,isConsolidated):
#     files = glob.glob(XBRL_FILES_URL + '*.xbrl')
#     for file in files:
#        print(getCompanyName(file))
