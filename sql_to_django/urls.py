from django.urls import path

from sql_to_django import views
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]