"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   28.04.2020 21:01
"""
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from environments import views

router = DefaultRouter()

router.register(r'environments', views.EnvironmentViewSet, basename='environment')

urlpatterns = [
    path('', include(router.urls))
]
