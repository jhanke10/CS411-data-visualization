from django.http import HttpResponse
from django.shortcuts import render
from project.models import Data
from rest_framework import viewsets
from final_project.serializers import DataSerializer

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

def api(request):
	return render(request, "api/index.html", context={}, )

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

class DataViewSet(viewsets.ModelViewSet):
	queryset = Data.objects.all()
	serializer_class = DataSerializer