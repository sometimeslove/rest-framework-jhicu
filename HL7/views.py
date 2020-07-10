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
        serializer.save()
        self.HIPMessageServer(serializer)
        serializer.instance.save()

    def HIPMessageServer(self,serializer):
        try:
            actionname = serializer.instance.ACTION_NAME;
            if actionname == "indept":
                self.InDeptBussiness(serializer)
            elif actionname == "outdept":
                self.OutDeptBussiness(serializer)
            elif actionname == "transdept":
                self.TransDeptBussiness(serializer)
            elif actionname == "transbed":
                self.TransbedBussiness(serializer)
            elif actionname == "order":
                self.OrderBussiness(serializer)
            else:
                self.InDeptBussiness(serializer)
        except:
            serializer.instance.RESULT='1'
    def InDeptBussiness(self, serializer):
        # path =os.path.abspath(os.curdir)+'\\HL7\\fixtures\\入科hl7消息报文.xml'
        # path = path.replace('\\','/')
        # strxml=""
        # with open(path,encoding='utf-8') as file:
        #     strxml = file.read()
        strxml = serializer.instance.MESSAGE_BODY;
        jcm = JHNIS_CARE_MAIN()
        hl7 = HL7Utils(jcm, strxml)
        hl7.ConvertInstance()
        jcm.save()
        serializer.instance.RESULT = '0'
        serializer.instance.PATIENT_ID = jcm.PATIENT_ID
        serializer.instance.VISIT_ID = jcm.VISIT_ID
        serializer.instance.INP_NO = jcm.INP_NO

    def OutDeptBussiness(self,serializer):
        pass
    def TransDeptBussiness(self,serializer):
        pass
    def TransbedBussiness(self,serializer):
        pass
    def OrderBussiness(self,serializer):
        pass

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
