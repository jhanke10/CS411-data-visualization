from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from project.models import Data, Source
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

#json parsing
import json

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
	# serializer = DataSerializer(data=json.loads(request.body))
	# if serializer.is_valid():
	# 	content = JSONRenderer().render(serializer.data)
	# 	stream = BytesIO(content)
	# 	data = JSONParser().parse(stream)
	# 	return Response(search_data(data))
	data = json.loads(request.body)
	#print(data)
	search = search_data(data)
	#print(search)
	return JsonResponse({"results": search})
	#return JsonResponse({"result": "test"})
	#return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def search_data(data):
	try:
		keys = data.keys()
		time_range = len(keys)
		sql = 'SELECT * FROM project_data WHERE'
		for i in range(len(keys)):
			if keys[i] == 'time_range':
				sql += ' create_time >= %s AND create_time <= %s'
				time_range = i
			if keys[i] == 'source_id':
				sql += ' source_id = %s'
			if i < len(keys) - 1:
				sql += ' AND'
		sql += ";"
		values = data.values()
		if time_range < len(keys):
			time1 = int(values[time_range].split('-')[0])
			time2 = int(values[time_range].split('-')[1])
			values[time_range] = time1
			values.insert(time_range + 1, time2)
		data_points = Data.objects.raw(sql, values)
		serializer = DataSerializer(data_points, many = True)
		return serializer.data
	except Data.DoesNotExist:
		raise HTTP_404_NOT_FOUND

def compare(request):
	data = json.loads(request.body)
	try:
		#sql = 'SELECT table.create_time, ABS(table.value1 - table.value2) FROM ((SELECT * AS (data_id1, source_id1, category, value1, create_time, upload_time) FROM project_data WHERE source_id = %s) NATURAL JOIN (SELECT * AS (data_id2, source_id2, category, value2, create_time, upload_time) FROM project_data WHERE source_id = %s)) AS table GROUP BY table.create_time'
		# sql = '''
		# 	SELECT data_id, value AS value1, create_time FROM project_data WHERE source_id = %s;
		# 	'''
		data_points = Data.objects.raw('SELECT data_id FROM project_data WHERE source_id = %s;', [data.values()[0]])
		serializer = DataSerializer(data_points, many = True)
		return JsonResponse({"data": serializer.data})
	except Data.DoesNotExist:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def linearRegression(request):
	if request.method == "GET":
		return JsonResponse({'test':123})
	elif request.method == "POST":
		try:
			print(request.body)
			data = json.loads(request.body)

			source_id1 = data["source_id1"]
			time1 = str(data["min_time1"]) + "-" + str(data["max_time1"])
			xSource = search_data({"source_id": source_id1, "time_range": time1})
			#print("X source:", xSource)

			source_id2 = data["source_id2"]
			time2 = str(data["min_time2"]) + "-" + str(data["max_time2"])
			ySource = search_data({"source_id": source_id2, "time_range": time2})

			k = data["k"]

			#TODO: Possibly handle this gracefully by removing start/end of one data set?
			if(len(xSource) != len(ySource)):
				return Resonse(status=status.HTTP_400_BAD_REQUEST)

			if k <= 0 or k > 5:
				return Response(status=status.HTTP_400_BAD_REQUEST)

			#Convert the resulting OrderedDict into a raw array of values
			xData = []
			yData = []
			for i in xSource:
				xData.append(i["value"])
			for i in ySource:
				yData.append(i["value"])

			#xSource = np.array([0, 1, 2, 3])
			#ySource = np.array([-1, 0.2, 0.9, 2.1])


			p = np.polyfit(xData, yData, k)

			#TODO: add error metrics
			return JsonResponse({'coefficients': p.tolist()})
		except KeyError as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

def linearRegressionData(request):
	data = json.loads(request.body)
	x = data["x"]
	y = data["y"]
	k = data["k"]
	p = np.polyfit(x, y, k)
	return JsonResponse({'coefficients': p.tolist()})

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
			newID = str(uuid.uuid4())
			with connection.cursor() as cur:
				cur.execute('INSERT INTO project_source (source_id, source_name) VALUES (%s, %s);', [newID, str(data['source_name'])])

			newObject = {
				"source_id": newID,
				"source_name": str(data['source_name'])
			}
			return Response(newObject, status=status.HTTP_201_CREATED)
		print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SourceDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
	queryset = Source.objects.raw('SELECT * FROM project_source')
	serializer_class = SourceSerializer

	def get_object(self, pk):
		try:
			return Source.objects.raw('SELECT * FROM project_source WHERE source_id = %s', [pk])
		except Source.DoesNotExist:
			raise HTTP_404_NOT_FOUND

	def get(self, request, pk, format = None):
		filteredObjects = self.get_object(pk)
		try:
			sources = filteredObjects[0]
			serializer = SourceSerializer(sources)
			return Response(serializer.data)
		except Exception as e:
			return Response("Yo, you found something that don't exist, foo'", status=status.HTTP_404_NOT_FOUND)

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
		filteredObjects = self.get_object(pk)
		try:
			source = filteredObjects[0]
			source.deleteSource()
			#TODO: when a source is deleted, delete all the data entries with the source_id
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			return Response("What you tried to delete doesn't exist.", status=status.HTTP_404_NOT_FOUND)

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
		#TODO: validate the source_id parameter and ensure it exists in the source table
		serializer = DataSerializer(data=request.data)
		print(request.data)
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			newID = str(uuid.uuid4())
			timeNow = int(time(datetime.now()))
			print(data)
			print(newID, str(request.data['source_id']), str(data['category']), int(data['value']), timeNow, int(data['create_time']))
			with connection.cursor() as cur:
				cur.execute('INSERT INTO project_data (data_id, source_id, category, value, upload_time, create_time) VALUES (%s, %s, %s, %s, %s, %s);', [newID, str(request.data['source_id']), str(data['category']), int(data['value']), timeNow, int(data['create_time']) ])
				#cur.execute('INSERT INTO project_data (data_id, source_id, category, value, upload_time, create_time) VALUES (%s, %s, %s, %s, %s, %s);', [str(uuid.uuid4()), str(data['source_id']), str(data['category'])])
			newObj = {
				"data_id": newID,
				"source_id": request.data['source_id'],
				"category": data['category'],
				"value": data['value'],
				"upload_time": timeNow,
				"create_time": data['create_time']
			}
			return Response(newObj, status=status.HTTP_201_CREATED)
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
		filteredObjects = self.get_object(pk)
		try:
			sources = filteredObjects[0]
			serializer = DataSerializer(sources)
			return Response(serializer.data)
		except Exception as e:
			return Response("Yo, you found something that don't exist, foo'", status=status.HTTP_404_NOT_FOUND)

	def put(self, request, pk, format=None):
		data_points = self.get_object(pk)[0]
		serializer = DataSerializer(data = request.data)
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			with connection.cursor() as cur:
				cur.execute('UPDATE project_data SET category = %s, value = %s, create_time = %s WHERE data_id = %s', [str(data['category']), int(data['value']), int(data['create_time']), pk])
			return Response(serializer.data)
		print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		filteredObjects = self.get_object(pk)
		try:
			data = filteredObjects[0]
			data.deleteData()
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			return Response("What you tried to delete doesn't exist.", status=status.HTTP_404_NOT_FOUND)
