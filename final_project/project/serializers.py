from project.models import Data
from rest_framework import serializers

class DataSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Data
		fields = ('category', 'value', 'source', 'time')
