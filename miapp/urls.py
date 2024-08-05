# miapp/urls.py
from django.urls import path
from .views import CustomLoginView, CustomLogoutView
from . import views

urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('', views.index_view, name='home'),
    path('updateUser/', views.updateUser_view, name='updateUser'),
    path('calificacion/', views.calificacion_view, name='calificacion'),
    path('asignatura/', views.asignatura_view, name='asignatura'),
    path('actividad/', views.actividad_view, name='actividad'),
    path('horario/', views.horario_view, name='horario'),
]


