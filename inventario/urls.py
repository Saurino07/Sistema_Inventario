from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_articulos, name='lista_articulos'),
    path('salida/<int:articulo_id>/', views.registrar_salida, name='registrar_salida'),
    path('responsiva/pdf/<int:responsiva_id>/', views.generar_pdf_responsiva, name='generar_pdf_responsiva'),
]