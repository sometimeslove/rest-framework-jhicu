import os
import xml.etree.ElementTree as ET
from HL7.models import *

class HL7Utils():
    model = ""
    xmlstr = ""
    namespace = {'urn':'urn:hl7-org:v3'}
    instace = ""
    def __init__(self,model,xml,namespace={}):
        self.model = model
        self.xmlstr = xml
        self.namespace = namespace or self.namespace

    def getInstance(self):
        root = ET.fromstring(self.xmlstr)
        instance = self.model
        path =os.path.abspath(os.curdir)+'\\HL7\\nodepathsetting.xml'
        path = path.replace('\\','/')
        config = ET.parse(path)
        root = config.getroot()
        nodeconfigs = root.findall("JHNIS_CARE_MAIN")

