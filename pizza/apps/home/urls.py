from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pizza.apps.home.views',
	url(r'^$', 'index_view', name = 'vista_principal'),
	url(r'^about/$', 'about_view', name = 'vista_about'),
	url(r'^productos/page/(?P<pagina>.*)/$', 'productos_view', name = 'vista_productos'),
	url(r'^categorias/page/(?P<pagina>.*)/$', 'categorias_view', name = 'vista_categorias'),
	url(r'^producto/(?P<id_prod>.*)/$', 'singleProduct_view', name = 'vista_single_producto'),
	url(r'^categoria/(?P<id_cate>.*)/$', 'singleCategoria_view', name = 'vista_single_categoria'),
	url(r'^contacto/$', 'contacto_view', name = 'vista_contacto'),
	url(r'^login/$', 'login_view', name= 'vista_login'),
	url(r'^logout/$', 'logout_view', name= 'vista_logout'),
	url(r'^registro/$', 'register_view', name= 'vista_registro'),
)