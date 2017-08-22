from xml.dom import minidom
import glob
from lxml import etree

CONSOLIDATED_TEXT="CurrentYearConsolidatedInstant"
NON_CONSOLIDATED_TEXT="CurrentYearNonConsolidatedInstant"



#write directory where xbrl files are
XBRL_FILES_URL="xbrls/"



def getValue(tagName,root,isConsolidated):
    nameSpaces = root.nsmap

    for nameSpace in nameSpaces:
        elements = root.findall(nameSpace+":"+tagName, nameSpaces)


        if(len(elements)==0):
            continue
        if (isConsolidated==True):
            for element in elements:
                if (element.get("contextRef") == CONSOLIDATED_TEXT):
                    return element.text
        else:
            for element in elements:
                if (element.get("contextRef") == NON_CONSOLIDATED_TEXT):
                    return element.text


#
# def getData(tagName,isConsolidated):
#     files = glob.glob(XBRL_FILES_URL + '*.xbrl')
#     for file in files:
#         print(file)
#         dom = minidom.parse(file)
#         root = etree.fromstring(dom.toxml())
#         getValue(tagName, root,isConsolidated)
