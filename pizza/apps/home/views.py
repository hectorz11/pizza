from django.shortcuts import render_to_response
from django.template import RequestContext
from pizza.apps.page.models import *
from pizza.apps.home.forms import ContactForm, LoginForm, RegisterForm
from django.core.mail import EmailMultiAlternatives # Enviando a HTML
from django.contrib.auth.models import User
import django

from pizza.settings import URL_LOGIN
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
# Paginacion en Django
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
import simplejson	# import json as simplejson

def index_view(request):
	return render_to_response('home/index.html', context_instance = RequestContext(request))

def about_view(request):
	version = django.get_version()
	mensaje = ""
	ctx = {'msg':mensaje,'version':version}
	return render_to_response('home/about.html', ctx, context_instance = RequestContext(request))

def productos_view(request,pagina):
	if request.method == "POST":
		if "product_id" in request.POST:
			try:
				id_producto = request.POST['product_id']
				p = producto.objects.get(pk=id_producto)
				mensaje = {"status":"True","product_id":p.id}
				p.delete() # Eliminamos objeto de la base de datos
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje = {"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	# select * from ventas_producto where status = True
	lista_prod = producto.objects.filter(status = True)
	paginator = Paginator(lista_prod,5) # Cuanto productos quieres por pagina = 3
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage):
		productos = paginator.page(paginator.num_pages)
	ctx = {'productos':productos}
	return render_to_response('home/productos.html', ctx, context_instance = RequestContext(request))

def categorias_view(request,pagina):
	if request.method == "POST":
		if "categoria_id" in request.POST:
			try:
				id_categoria = request.POST['categoria_id']
				p = categoriaProducto.objects.get(pk=id_categoria)
				mensaje = {"status":"True","categoria_id":p.id}
				p.delete() # Eliminamos objeto de la base de datos
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje = {"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	# select * from ventas_producto where status = True
	lista_prod = categoriaProducto.objects.filter(status = True)
	paginator = Paginator(lista_prod,5) # Cuanto productos quieres por pagina = 3
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		categorias = paginator.page(page)
	except (EmptyPage,InvalidPage):
		categorias = paginator.page(paginator.num_pages)
	ctx = {'categorias':categorias}
	return render_to_response('home/categorias.html', ctx, context_instance = RequestContext(request))

def singleProduct_view(request,id_prod):
	prod = producto.objects.get(id=id_prod)
	cats = prod.categorias.all() # Obteniendo la(s) categoria(s) del producto encontrado
	ctx = {'producto':prod,'categorias':cats}
	return render_to_response('home/SingleProducto.html', ctx, context_instance= RequestContext(request))

def singleCategoria_view(request,id_cate):
	if request.method == "POST":
		if "producto_id" in request.POST:
			try:
				id_producto = request.POST['producto_id']
				p = Producto.objects.get(pk=id_producto)
				mensaje = {"status":"True","producto_id":p.id}
				p.delete()
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje = {"status":"False"}
	prod = categoriaProducto.objects.get(id=id_cate)
	valor1 = prod.producto_set.all()
	ctx = {'categoriaProducto':prod,'resultados':valor1}
	return render_to_response('home/SingleCategoria.html',ctx,context_instance=RequestContext(request))

@login_required(login_url=URL_LOGIN)
def contacto_view(request):
	info_enviado = False # Definir si se envio la informacion o no se envio
	email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']

			# Configuracion enviada mensaje via GMAIL
			to_admin = 'hector.rz11@gmail.com'
			html_content = "Informacion recibida de [%s] <br><br><br>***Mensaje****<br><br>%s"%(email,texto)
			msg = EmailMultiAlternatives('Correo de Contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html') #Definimos el contenido como HTML
			msg.send() # Enviamos el correo
	else:
		formulario = ContactForm()
	ctx = {'form':formulario,'email':email,'titulo':titulo,'texto':texto,'info_enviado':info_enviado}
	return render_to_response('home/contacto.html', ctx, context_instance = RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				next = request.POST['next']
				#print "recibido desde POST %s"%next
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username, password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect(next)
				else:
					mensaje = "usuario y/o password incorrecto"
		next = request.REQUEST.get('next')
		#print "la url es %s"%next
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje,'next':next}
		return render_to_response('home/login.html',ctx,context_instance = RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save()
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))