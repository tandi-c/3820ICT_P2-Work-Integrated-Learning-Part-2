from django.urls import path
from django.conf.urls import url
from .views import (
    ClientListView, ClientDetailView, ClientCreateView, 
    ClientUpdateView, ClientDeleteView, ClientUploadView, 
    ClientVideoView, ClientPoseVideoView, VideoDeleteView
)
from . import views

urlpatterns = [
    path('', ClientListView.as_view(), name='page-home'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client'),
    path('create-client/', ClientCreateView.as_view(), name='create-client'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='update-client'),
    path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='delete-client'),
    path('client/<int:pk>/upload-video/', ClientUploadView.as_view(), name='upload-video'),
    path('client/<int:pk>/video-modal/<int:video_pk>/', ClientVideoView.as_view(), name='video-modal'),
    path('client/<int:pk>/pose-video-modal/<int:video_pk>/', ClientPoseVideoView.as_view(), name='pose-video-modal'),
    path('client/<int:pk>/view-pdf/<str:path>/', views.pdf_view, name='pdf-view'), 
]
