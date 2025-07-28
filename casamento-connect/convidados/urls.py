from django.urls import path
from . import views
urlpatterns = [
    path('', views.convidados, name='convidados'),
    path('lista_convidados', views.lista_convidados, name='lista_convidados'),
    path('responder_presenca/', views.responder_presenca, name='responder_presenca'),
    path('reservar_presente/<int:id>', views.reservar_presente, name='reservar_presente'),
]
