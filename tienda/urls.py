from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos_lista, name='productos_lista'),
    path('producto/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('busqueda-ajax/', views.busqueda_ajax, name='busqueda_ajax'),
]