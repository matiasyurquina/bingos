from django.contrib import admin
from django.urls import path
from bingos.views import buscar#, home
from django.conf.urls import handler500, handler404
from admin_manager import views

# from django.urls.conf import include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from django.views.defaults import page_not_found

#handler404 = 'admin_manager.views.error_404'  # Cambia esto a la ruta correcta
#handler500 = 'admin_manager.views.error_404'    # Opcional, para el error 500



urlpatterns = [
    path('', buscar, name="home"),
    path('verificar_carton/', buscar, name="buscar"),
    # path('ip/', ip),
    path('admin/', views.home, name="admin_home"),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/publicidad/', views.publicidad_view, name="publicidad"),
    path('admin/publicidad/nueva/', views.pub_crear, name="publicidad_nueva"),
    path('admin/publicidad/editar/', views.pub_editarShow, name="publicidad_editarShow"),
    path('admin/publicidad/editar/<int:id>/', views.pub_editar, name="publicidad_editar"),

    path('admin/bingos/', views.bingos_menu, name="bingos_menu"),
    path('admin/bingos/nuevo/', views.bingos_nuevo, name="bingos_nuevo"),
    path('admin/bingos/editar/', views.bingos_editarShow, name="bingos_editarShow"),
    path('admin/bingos/editar/<int:id>/', views.bingos_editar, name="bingos_editar"),

    path('admin/carton/', views.carton_menu, name="carton_menu"),
    path('admin/carton/editar/', views.carton_show, name="cartones_show"),
    path('admin/carton/editar/<int:id>/', views.carton_editar, name="cartones_editar"),
    path('admin/carton/editar/<int:id>/<int:idCarton>', views.carton_editarCarton, name="cartones_editarCarton"),
    path('admin/carton/subir/', views.carton_subir, name="cartones_subir"),
    path('admin/carton/subir/<int:id>/', views.carton_subirVer, name="cartones_subirVer"),
]

handler404 = 'admin_manager.views.handler404'
handler500 = 'admin_manager.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += [path('404/', page_not_found, {'exception': Exception('Página no encontrada')}, name='404')]
