from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.lista_articulos, name='lista_articulos'),
    path('articulo/nuevo/', views.crear_articulo, name='crear_articulo'),
    path('articulo/editar/<int:articulo_id>/', views.editar_articulo, name='editar_articulo'),
    path('salida/<int:articulo_id>/', views.registrar_salida, name='registrar_salida'),
    path('responsivas/', views.historial_responsivas, name='historial_responsivas'),
    path('responsiva/pdf/<int:responsiva_id>/', views.generar_pdf_responsiva, name='generar_pdf_responsiva'),
    path('accounts/login/', include('django.contrib.auth.urls')),
    path('accounts/logout/', views.cerrar_sesion, name='logout'),
]