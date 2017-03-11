from django.http import HttpResponse
from django.shortcuts import render

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
