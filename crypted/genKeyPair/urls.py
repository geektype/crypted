from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download-public', views.downloadPublic, name='downloadPublic'),
    path('download-private', views.downloadPrivate, name='downloadPrivate')
]
