from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('tomorrow', views.tomorrow),
    path('three_days', views.three_days),
    path('seven_days', views.seven_days)
]
