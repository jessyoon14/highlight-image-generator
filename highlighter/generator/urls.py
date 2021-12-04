from django.urls import path

from . import views

urlpatterns = [
    path('generator/', views.index, name='index'),
    path('downloader/', views.download, name='download')
]

