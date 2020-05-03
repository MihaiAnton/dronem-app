"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   02.05.2020 19:57
"""
from django.urls import path

from rl import views

urlpatterns = [
    path('rl/train/', views.TrainView.as_view(), name='train-view')
]
