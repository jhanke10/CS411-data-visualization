from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from project.models import Data, Source, User
from .serializers import DataSerializer, SourceSerializer
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

#numpy
import numpy as np
import scipy as sp

start = datetime.utcfromtimestamp(0)

def time(time):
	return (time - start).total_seconds() * 1000.0

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

def linearRegression(request):
	if request.method == "GET":
		return JsonResponse({'test':123})
	elif request.method == "POST":
		try:
			source_id1 = request.POST.get("source_id1")
			min_time1 = request.POST.get("min_time1")
			max_time1 = request.POST.get("max_time1")

			source_id2 = request.POST.get("source_id2")
			min_time2 = request.POST.get("min_time2")
			max_time2 = request.POST.get("max_time2")

			k = request.POST.get("k")

			#Execute the SQL search with above parameters to get x and y

			xSource = np.array([0, 1, 2, 3])
			ySource = np.array([-1, 0.2, 0.9, 2.1])
			k = 1

			if xSource.shape[0] != ySource.shape[0]:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			if k <= 0 or k > 5:
				return Response(status=status.HTTP_400_BAD_REQUEST)

			p = np.polyfit(xSource, ySource, k)

			#TODO: add error metrics
			return JsonResponse({'coefficients': p.tolist()})
		except KeyError as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class SourceList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
	queryset = Source.objects.raw('SELECT * FROM project_source')
	serializer_class = SourceSerializer

	def get(self, request, format = None):
		data_points = Source.objects.raw('SELECT * FROM project_source')
		serializer = SourceSerializer(data_points, many = True)
		return Response(serializer.data)

	def post(self, request, format = None):
		serializer = SourceSerializer(data=request.data)
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			with connection.cursor() as cur:
				cur.execute('INSERT INTO project_source (source_id, source_name, user) VALUES (%s, %s, %s);', [str(uuid.uuid4), str(data['source_name']), str(data['user'])])
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SourceDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
	queryset = Source.objects.raw('SELECT * FROM project_source')
	serializer_class = SourceSerializer

	def get_object(self, pk):
		try:
			return Data.objects.raw('SELECT * FROM project_source WHERE source_id = %s', [pk])
		except Data.DoesNotExist:
			raise HTTP_404_NOT_FOUND

	def get(self, request, pk, format = None):
		sources = self.get_object(pk)[0]
		serializer = SourceSerializer(sources)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		serializer = SourceSerializer(data = request.data)
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			with connection.cursor() as cur:
				cur.execute('UPDATE project_source SET source_name = %s WHERE source_id = %s', [str(data['source_name']), pk])
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		source = self.get_object(pk)[0]
		source.deleteSource()
		return Response(status=status.HTTP_204_NO_CONTENT)

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
				cur.execute('INSERT INTO project_data (data_id, source, category, value, time) VALUES (%s, %s, %s, %d, %d);', [str(uuid.uuid4), str(data['source']), str(data['category']), int(data['value']), int(time(datetime.now()))])
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
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			with connection.cursor() as cur:
				cur.execute('UPDATE project_data SET category = %s, value = %d WHERE data_id = %s', [str(data['category']), int(data['value']), pk])
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		data = self.get_object(pk)[0]
		data.deleteData()
		return Response(status=status.HTTP_204_NO_CONTENT)
