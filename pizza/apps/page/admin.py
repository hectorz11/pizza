from django.contrib import admin
from pizza.apps.page.models import cliente, producto, categoriaProducto, carrito

class productoAdmin(admin.ModelAdmin):
	list_display 	= ('nombre','thumbnail','precio')
	list_filter 	= ('categorias','precio')
	search_fields 	= ['nombre','precio']
	fields 			= ('nombre','descripcion',('precio','imagen'),'categorias','status')

admin.site.register(cliente)
admin.site.register(producto,productoAdmin)
admin.site.register(categoriaProducto)
admin.site.register(carrito)