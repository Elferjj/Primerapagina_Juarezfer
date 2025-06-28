from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages # Para mensajes de éxito/error
from .forms import ClienteForm, ProductoForm, SucursalForm, VendedorForm, BusquedaForm
from .models import Cliente, Producto, Sucursal, Vendedor
from django.db.models import Q # Para búsquedas OR
from django.contrib.auth.decorators import login_required # Para el perfil
from django.contrib.auth.forms import UserChangeForm # Para modificar usuario base de Django
from django.contrib.auth.models import User # Para el modelo de usuario base

def home(request):
    return render(request, 'myapp/home.html')

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente guardado con éxito!')
            return redirect('crear_cliente') # Redirige a la misma página para un nuevo formulario
    else:
        form = ClienteForm()
    return render(request, 'myapp/form_cliente.html', {'form': form, 'titulo': 'Crear Cliente'})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto guardado con éxito!')
            return redirect('crear_producto')
    else:
        form = ProductoForm()
    return render(request, 'myapp/form_producto.html', {'form': form, 'titulo': 'Crear Producto'})

def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal guardada con éxito!')
            return redirect('crear_sucursal')
    else:
        form = SucursalForm()
    return render(request, 'myapp/form_sucursal.html', {'form': form, 'titulo': 'Crear Sucursal'})

def crear_vendedor(request):
    if request.method == 'POST':
        form = VendedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendedor guardado con éxito!')
            return redirect('crear_vendedor')
    else:
        form = VendedorForm()
    return render(request, 'myapp/form_vendedor.html', {'form': form, 'titulo': 'Crear Vendedor'})


def buscar_resultados(request):
    form = BusquedaForm(request.GET or None)
    resultados = {
        'clientes': [],
        'productos': [],
        'sucursales': [],
        'vendedores': []
    }
    query = None

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            # Búsqueda en Clientes por nombre o apellido
            resultados['clientes'] = Cliente.objects.filter(
                Q(nombre__icontains=query) | Q(apellido__icontains=query)
            )
            # Búsqueda en Productos por nombre o descripción
            resultados['productos'] = Producto.objects.filter(
                Q(nombre__icontains=query) | Q(descripcion__icontains=query)
            )
            # Búsqueda en Sucursales por nombre o dirección
            resultados['sucursales'] = Sucursal.objects.filter(
                Q(nombre__icontains=query) | Q(direccion__icontains=query)
            )
            # Búsqueda en Vendedores por nombre, apellido o código de empleado
            resultados['vendedores'] = Vendedor.objects.filter(
                Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(codigo_empleado__icontains=query)
            )

    return render(request, 'myapp/resultados_busqueda.html', {
        'form': form,
        'resultados': resultados,
        'query': query
    })

def about(request):
    context = {
        'creador_nombre': 'Juarez Fernando Gabriel',
        'creador_profesion': 'Policía de la Provincia de Buenos Aires',
        'dedicacion_curso': 'dedicó mucho tiempo y dedicación al curso.',
        'objetivo_web': 'Básicamente quería crear una web donde personas puedan encontrarse en una sucursal de videojuegos y poder hacer ventas de sus productos electrónicos.'
    }
    return render(request, 'myapp/about.html', context)