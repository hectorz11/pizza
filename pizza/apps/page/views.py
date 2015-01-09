from django.shortcuts import render_to_response
from django.template import RequestContext
from pizza.apps.page.forms import addProductForm,addCarritoForm
from pizza.apps.page.models import producto,carrito
from django.http import HttpResponseRedirect

def add_product_view(request):
	info = "iniciado"
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES)
		if form.is_valid():
			add = form.save(commit=False)
			add.status = True
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones de ManyToMany
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/producto/%s'%add.id)
	else:
		form = addProductForm()
	ctx = {'form':form, 'informacion':info}
	return render_to_response('page/addProducto.html',ctx,context_instance = RequestContext(request))

def add_carrito_view(request):
	info = "iniciado"
	if request.method == "POST":
		form = addCarritoForm(request.POST,request.FILES)
		if form.is_valid():
			add = form.save(commit=False)
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones de ManyToMany
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/productos/page/1')
	else:
		form = addCarritoForm()
	ctx = {'form':form, 'informacion':info}
	return render_to_response('page/addCarrito.html',ctx,context_instance = RequestContext(request))

def edit_product_view(request,id_prod):
	info = "iniciado"
	prod = producto.objects.get(pk=id_prod)
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES,instance=prod)
		if form.is_valid():
			edit_prod = form.save(commit=False)
			form.save_m2m()
			edit_prod.status = True
			edit_prod.save() # Guardamos el objeto
			info = "Correcto"
			return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
	else:
		form = addProductForm(instance=prod)
	ctx = {'form':form, 'informacion':info}
	return render_to_response('page/editProducto.html',ctx,context_instance=RequestContext(request))