from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('pizza.apps.page.views',
	url(r'^add/producto/$','add_product_view',name="vista_agregar_producto"),
	url(r'^add/carrito/$','add_carrito_view',name="vista_agregar_carrito"),
	url(r'^edit/producto/(?P<id_prod>.*)/$','edit_product_view',name="vista_editar_producto"),
)