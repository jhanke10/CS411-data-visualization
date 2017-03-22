from django.http import HttpResponse
from django.shortcuts import render
from project.models import Data
from .serializers import DataSerializer
from django.utils.six import BytesIO
from datetime import datetime
from django.db import connection

#REST Framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView

def index(request):
	return render(request, "main/index.html", context={}, )

def realtime(request):
	return render(request, "realtime/index.html", context={}, )

def visualization(request):
	return render(request, "visualization/index.html", context={}, )

def predictive(request):
	return render(request, "predictive/index.html", context={}, )

class DataList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
	queryset = Data.objects.raw('SELECT * FROM project_data')
	serializer_class = DataSerializer

	def get(self, request, format = None):
		data_points = Data.objects.raw('SELECT * FROM project_data')
		serializer = DataSerializer(data_points, many = True)
		return Response(serializer.data)

	def post(self, request, format = None):
		serializer = DataSerializer(data=request.data)
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			with connection.cursor() as cur:
				cur.execute('INSERT INTO project_data (category, value, source, time) VALUES (%s, %s, %s, %s);', [str(data['category']), int(data['value']), str(data['source']), datetime.now()])
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
	queryset = Data.objects.raw('SELECT * FROM project_data')
	serializer_class = DataSerializer

	def get_object(self, pk):
		try:
			return Data.objects.raw('SELECT * FROM project_data WHERE id = %s', [pk])
		except Data.DoesNotExist:
			raise HTTP_404_NOT_FOUND

	def get(self, request, pk, format = None):
		data_points = self.get_object(pk)[0]
		serializer = DataSerializer(data_points)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		data_points = self.get_object(pk)[0]
		serializer = DataSerializer(data = request.data)
		print serializer
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			with connection.cursor() as cur:
				cur.execute('UPDATE project_data SET category = %s, value = %s, source = %s, time = %s WHERE id = %s', [str(data['category']), int(data['value']), str(data['source']), datetime.now(), pk])
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		data = self.get_object(pk)[0]
		data.deleteData()
		return Response(status=status.HTTP_204_NO_CONTENT)