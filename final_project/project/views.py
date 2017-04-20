from django.http import HttpResponse
from django.shortcuts import render
from project.models import Data, Source, User
from .serializers import DataSerializer
from django.utils.six import BytesIO
from datetime import datetime
from django.db import connection
import uuid

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

def search(request):
	serializer = DataSerializer(data=request.data)
	if serializer.is_valid():
		content = JSONRenderer().render(serializer.data)
		stream = BytesIO(content)
		data = JSONParser().parse(stream)
		try:
			keys = data.keys()
			time_range = len(keys)
			sql = 'SELECT * FROM project_data WHERE'
			for i in range(len(keys)):
				if keys[i] == 'time_range':
					sql += ' ' + keys[i] + ' >= %s AND ' + keys[i] + ' <= %s'
					time_range = i
				else:
					sql += ' ' + keys[i] + ' = %s'
				if i < len(keys) - 1:
					sql += ' AND'
			values = data.values()
			if time_range < len(keys):
				time1 = int(values[time_range].split('-')[0])
				time2 = int(values[time_range].split('-')[1])
				values[time_range] = time1
				values.insert(time_range + 1, time2)
			data_points = Data.objects.raw(sql, values)
			serializer = DataSerializer(data_points, many = True)
			return Response(serializer.data)
		except Data.DoesNotExist:
			raise HTTP_404_NOT_FOUND
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def compare(request):
	serializer = DataSerializer(data=request.data)
	if serializer.is_valid():
		content = JSONRenderer().render(serializer.data)
		stream = BytesIO(content)
		data = JSONParser().parse(stream)
		try:
			keys = data.keys()
			sql = 'SELECT table.time, table.value1 - table.value2 FROM (SELECT * AS (data_id1, source_id1, user_id, category, value1, time) FROM project_data WHERE source_id = %s) NATURAL JOIN (SELECT * AS (data_id2, source_id2, user_id, category, value2, time) FROM project_data WHERE source_id = %s) AS table GROUP BY table.time'
			values = data.values()
			data_points = Data.objects.raw(sql, values)
			serializer = DataSerializer(data_points, many = True)
			return Response(serializer.data)
		except Data.DoesNotExist:
			raise HTTP_404_NOT_FOUND
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
				cur.execute('INSERT INTO project_data (source_id, category, value, time) VALUES (%s, %s, %s, %s);', [UUID(str(data['source'])), str(data['category']), int(data['value']), datetime.now()])
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
			return Data.objects.raw('SELECT * FROM project_data WHERE data_id = %s', [pk])
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
				cur.execute('UPDATE project_data SET source_id = %s, category = %s, value = %s, time = %s WHERE data_id = %s', [UUID(str(data['source'])), str(data['category']), int(data['value']), datetime.now(), pk])
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		data = self.get_object(pk)[0]
		data.deleteData()
		return Response(status=status.HTTP_204_NO_CONTENT)