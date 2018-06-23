from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # -------------------------------------------------------------------------------
    # URLs para los usuarios
    # -------------------------------------------------------------------------------
    url(r'^usuarios/lista/$', views.user_list, name='user_list'),
    url(r'^usuarios/nuevo/$', views.new_user, name='new_user'),
    url(r'^usuarios/editar/(?P<pk>[0-9]+)/$', views.edit_user, name='edit_user'),
    url(r'^usuarios/borrar/(?P<pk>[0-9]+)/$', views.delete_user, name='delete_user'),
    url(r'^usuarios/info/(?P<pk>[0-9]+)/$', views.user_info, name='user_info'),
    # -------------------------------------------------------------------------------
    # URLs para los lugares
    # -------------------------------------------------------------------------------
    url(r'^lugares/lista/(?P<tp>[a-z]+)/$', views.place_list, name='place_list'),
    url(r'^lugares/nuevo/(?P<tp>[a-z]+)/$', views.new_place, name='new_place'),
    url(r'^lugares/editar/(?P<pk>[0-9]+)/$', views.edit_place, name='edit_place'),
    url(r'^lugares/borrar/(?P<pk>[0-9]+)/(?P<list>[a-z]+)/$', views.delete_place, name='delete_place'),
    url(r'^lugares/info/(?P<pk>[0-9]+)/$', views.place_info, name='place_info'),
    url(r'^X/$', TemplateView.as_view(template_name='nolugares.html'), name='nolugares'),
    # -------------------------------------------------------------------------------
    # URLs para administración
    # -------------------------------------------------------------------------------
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^stop/$', TemplateView.as_view(template_name='denied.html'), name='denied'),
    url(r'^roladmin/(?P<pk>[0-9]+)/$', views.addtoadmin, name='addtoadmin'),
    url(r'^rolusers/(?P<pk>[0-9]+)/$', views.addtousers, name='addtousers'),
    # -------------------------------------------------------------------------------
    # URLs de funcionamiento de la aplicación
    # -------------------------------------------------------------------------------
    url(r'^$', views.home, name='home'),
    url(r'^favoritos/$', views.favoritos, name='favoritos'),
    url(r'^votos/$', views.votos, name='votos'),
    url(r'^ayuda/$', TemplateView.as_view(template_name='ayuda.html'), name='ayuda'),
    url(r'^galeria/(?P<pk>[0-9]+)/$', views.galery, name='galery'),
    url(r'^galeria/add/(?P<pk>[0-9]+)/$', views.add_photo, name='add_photo'),
    url(r'^galeria/del/(?P<pk>[0-9]+)/$', views.del_photo, name='del_photo'),
    url(r'^recomendaciones/$', views.recomend, name='recomend'),
    url(r'^recomendaciones/resultados/$', views.recomendaciones, name='recomendaciones'),
    # -------------------------------------------------------------------------------
    # URLs para la web API
    # -------------------------------------------------------------------------------
    url(r'^getSites/$', views.getSites, name='getSites'),
    url(r'^getPlaceDetails/$', views.getPlaceDetails, name='getPlaceDetails'),
    url(r'^getRecommendations/$', views.getRecommendations, name='getRecommendations'),
    url(r'^setFavorite/$', views.setFavorite, name='setFavorite'),
    url(r'^setFeedback/$', views.setFeedback, name='setFeedback'),
    url(r'^createUser/$', views.createUser, name='createUser'),
    url(r'^deleteUser/$', views.deleteUser, name='deleteUser'),


    url(r'^mapa/$', TemplateView.as_view(template_name='mapa.html'), name='mapa'),
    url(r'^test/$', TemplateView.as_view(template_name='test.html'), name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
