import os

from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from HL7.models import JHNIS_CARE_MAIN
from HL7.permissions import IsOwnerOrReadOnly
from HL7.serializers import HL7Serializer, UserSerializer
import xml.etree.ElementTree as ET
from HL7.HL7Utils import HL7Utils

class HL7ViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = JHNIS_CARE_MAIN.objects.all()
    serializer_class = HL7Serializer
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly, )

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)
        serializer.save()
        hl7xml = serializer.instance.MESSAGE_BODY;

        path =os.path.abspath(os.curdir)+'\\HL7\\fixtures\\入科hl7消息报文.xml'
        path = path.replace('\\','/')
        strxml=""
        with open(path,encoding='utf-8') as file:
            strxml = file.read()
        jcm = JHNIS_CARE_MAIN()
        jcm.APPLY_ID=222
        hl7 = HL7Utils(jcm,strxml)
        ret = hl7.getInstance()
        ret.save()
        doc = ET.parse(path)
        # doc = ET.fromstring(strxml)
        root = doc.getroot()
        print(root.tag,"|",root.attrib)
        # namespaces = {'HL7': 'urn:hl7-org:v3','xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        namespace = {'urn':'urn:hl7-org:v3'}
        for child in root:
            print(child.tag,"|",child.text)
        # node = root.find('{urn:hl7-org:v3}'+'id')
        node = root.find('urn:id',namespace)
        print(node.tag)
        print(node.text)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
