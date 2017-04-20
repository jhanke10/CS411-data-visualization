from project.models import Data, Source
from rest_framework import serializers

class DataSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Data
		fields = ('data_id', 'source_id', 'category', 'value', 'upload_time', 'create_time')

class SourceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Source
		fields = ('source_id', 'source_name')

# class UserSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ('user_id', 'username', 'password')
