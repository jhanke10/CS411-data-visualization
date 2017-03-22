import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
#from project.models import Data
from rest_framework import viewsets
from .serializers import NumericalDataSerializer

from project.models import NumericalData

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from django.utils.six import BytesIO
from datetime import datetime

def index(request):
	return render(
		request,
		"main/index.html",
		context={},
	)

def realtime(request):
	return render(request, "realtime/index.html", context={}, )

def visualization(request):
	return render(request, "visualization/index.html", context={}, )

def predictive(request):
	return render(request, "predictive/index.html", context={}, )

def search(request):
	return render(request, "search/index.html", context={}, )

# def api(request):
# 	return render(request, "api/index.html", context={}, )

@api_view(['GET', 'POST'])
def api(request):
	if request.method == "GET":
		'''
		allData = NumericalData.objects.values()
		print("Printing all data")
		print(allData)
		for record in allData:
			#print(record.first, record.second)
			print(str(record))
		#return JsonResponse(json.dumps(list(allData)))
		return HttpResponse("Testing in progress")
		'''

		allData = NumericalData.objects.all()
		serializer = NumericalDataSerializer(allData, many=True)

		#Try to, for example, return all unique names of entries when GET UNIQUE is called
		return JsonResponse(serializer.data, safe=False)
	elif request.method == "POST":
		print("POST request with data=", request.data)
		serializer = NumericalDataSerializer(data=request.data)
		if serializer.is_valid():
			content = JSONRenderer().render(serializer.validated_data)
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			#with connection.cursor() as cur:
			#	cur.execute('INSERT INTO project_data (dataID, name, time, value) VALUES (%s, %s, %s, %s);', [str(data['dataID']), int(data['name']), datetime.now(), str(data['value'])])
			serializer.save()
			#data = NumericalData.objects.raw('SELECT * FROM project_data')
			#serializer = NumericalDataSerializer(data, many=True)
			return Response(serializer.data)
		else:
			return Response(
				serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'POST'])
# def data_list(request):
#     """
#     List all tasks, or create a new data.
#     """
#     if request.method == 'GET':
#         data = Data.objects.raw('SELECT * FROM project_data')
#         serializer = DataSerializer(data, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = DataSerializer(data=request.data)
#         if serializer.is_valid():
#             content = JSONRenderer().render(serializer.data)
#             stream = BytesIO(content)
#             data = JSONParser().parse(stream)
#             with connection.cursor() as cur:
#                 cur.execute('INSERT INTO project_data (category, value, source, time) VALUES (%s, %s, %s, %s);', [str(data['category']), int(data['value']), str(data['source']), datetime.now()])
#             # serializer.save()
#             # data = Data.objects.raw('SELECT * FROM project_data')
#         	# serializer = DataSerializer(data, many=True)
#         	return Response(serializer.data)
#         else:
#             return Response(
#                 serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def data_detail(request, pk):
#     """
#     Get, udpate, or delete a specific data
#     """
#     try:
#         data = Data.objects.raw('SELECT * FROM project_data WHERE id = %s', [pk])
#     except Data.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = DataSerializer(data)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = DataSerializer(data, data=request.data)
#         if serializer.is_valid():
#             content = JSONRenderer().render(serializer.data)
#             stream = BytesIO(content)
#             data = JSONParser().parse(stream)
#             with connection.cursor() as cur:
#                 cur.execute('UPDATE project_data SET category = %s, value = %s, source = %s, time = %s WHERE id = %s', [str(data['category']), int(data['value']), str(data['source']), datetime.datetime.strptime(str(data['time']), "%Y-%m-%dT%H:%M:%S.%f"), pk])
#             # serializer.save()
#             # data = Data.objects.raw('SELECT * FROM data_data')
#         	# serializer = DataSerializer(data, many=True)
#         	return Response(serializer.data)
#         else:
#             return Response(
#                 serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         data.deleteData()
#         return Response(status=status.HTTP_204_NO_CONTENT)

'''
class DataList(generics.ListCreateAPIView):
	queryset = Data.objects.all()
	serializer_class = DataSerializer

class DataDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Data.objects.all()
	serializer_class = DataSerializer
	'''


# class DataViewSet(viewsets.ModelViewSet):
# 	queryset = Data.objects.all()
# 	serializer_class = DataSerializer
