from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('<int:attendance_id>/update/', views.attendance_update, name='attendance_update'),
]