from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from HL7.models import JHINIS_CARE_MAIN
from HL7.permissions import IsOwnerOrReadOnly
from HL7.serializers import HL7Serializer, UserSerializer


class HL7ViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = JHINIS_CARE_MAIN.objects.all()
    serializer_class = HL7Serializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly, )

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
