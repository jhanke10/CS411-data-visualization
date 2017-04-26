"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

#REST Framework
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from project import views as projectViews

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', projectViews.index, name='index'),
  url(r'^main/', projectViews.index, name='index'),
  url(r'^realtime/', projectViews.realtime),
  url(r'^visualization/', projectViews.visualization),
  url(r'^predictive/', projectViews.predictive),
  url(r'^api/data/$', projectViews.DataList.as_view()),
  #url(r'^api/data/(?P<pk>[-\w]+)/$', projectViews.DataDetail.as_view()),
  url(r'^api/data/(?P<pk>.*)/$', projectViews.DataDetail.as_view()),
  url(r'^api/user/$', projectViews.UserList.as_view()),
  url(r'^api/user/(?P<pk>.*)/$', projectViews.UserDetail.as_view()),
  url(r'^api/source/$', projectViews.SourceList.as_view()),
  #url(r'^api/source/(?P<pk>[-\w ]+)/$', projectViews.SourceDetail.as_view()),
  url(r'^api/source/(?P<pk>.*)/$', projectViews.SourceDetail.as_view()),
  url(r'^api/search/$',projectViews.search),
  url(r'^api/compare/$',projectViews.compare),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^api/predict/linear/', projectViews.linearRegression),
  url(r'^api/predict/linearData/', projectViews.linearRegressionData),
]

urlpatterns = format_suffix_patterns(urlpatterns)
