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

    def ConvertInstance(self):
        doc = ET.fromstring(self.xmlstr)
        instance = self.model
        path =os.path.abspath(os.curdir)+'\\HL7\\nodepathsetting.xml'
        path = path.replace('\\','/')
        config = ET.parse(path)
        root = config.getroot()
        for field in self.model.__dict__:
            nodePATH = root.find(self.model.__class__.__name__+'/'+field+'/NodePath')
            nodeATTR = root.find(self.model.__class__.__name__+'/'+field+'/AttributName')
            attr=''
            if nodePATH is not None:
                if nodeATTR is not None:
                    attr = nodeATTR.text
                self.model.__dict__[field]=self.getNodeValue(nodePATH.text,doc,attr)
        return self.model

    def getNodeValue(self,path,doc,attrib):
        rootName = doc.tag
        for i in ["{"+ value+"}" for key,value in self.namespace.items()]:
            rootName = rootName.replace(i,'')
        if path.startswith('/'+rootName):
            path = path.replace('/'+rootName,'')
        if self.namespace is not None:
            prefix = list(self.namespace.keys())[0]
            path = path.replace('/','/'+prefix+':')
        path = path.lstrip('/')

        node = doc.find(path,self.namespace)
        if node is None:
            return ""
        if attrib=='':
            return node.text
        else:
            return node.attrib[attrib]