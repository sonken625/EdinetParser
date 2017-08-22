from xml.dom import minidom
import glob
from lxml import etree

NAME_SPACES={}
CONSOLIDATED_TEXT="CurrentYearConsolidatedInstant"
NON_CONSOLIDATED_TEXT="CurrentYearNonConsolidatedInstant"

#write directory where xbrl files are
XBRL_FILES_URL="test/"

def getValue(tagName,root,isConsolidated):
    for NAME_SPACE in NAME_SPACES:
        elements = root.findall(NAME_SPACE+":"+tagName, NAME_SPACES)
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



files=glob.glob(XBRL_FILES_URL+'*.xbrl')
print(files[0])
dom = minidom.parse(files[0])
root = etree.fromstring(dom.toxml())
NAME_SPACES = root.nsmap

print(getValue("AccumulatedDepreciationWells",root,True))

