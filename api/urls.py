from django.urls import path
from api import views

urlpatterns = [
    path('search/', views.search, name='api'),
    path('cluster/', views.cluster, name='api'),
]