from django.contrib.auth.models import User
from rest_framework import serializers

from HL7.models import HL7_MESSAGE_LOGS


class HL7Serializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(
    #     view_name='snippet-highlight', format='html')

    class Meta:
        model = HL7_MESSAGE_LOGS
        fields = ('MESSAGE_BODY', 'CREATE_USER')
        # fields = ('__all__')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ( 'id','username')
