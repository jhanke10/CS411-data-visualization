from project.models import Data, Source, User
from rest_framework import serializers

class DataSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Data
		fields = ('data_id', 'source', 'category', 'value', 'time')

class SourceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Source
		fields = ('source_id', 'source_name', 'user')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('user_id', 'username', 'password')
