from project.models import NumericalData
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')

class NumericalDataSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = NumericalData
		fields = ('dataID', 'name', 'time', 'value')
