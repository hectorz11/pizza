from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('pizza.apps.webServices.wsProductos.views',
		url(r'^ws/productos/$','wsProductos_view',name="ws_productos_url"),
)