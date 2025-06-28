from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages # Para mensajes de éxito/error
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import ClienteForm, ProductoForm, SucursalForm, VendedorForm, BusquedaForm
from .models import Cliente, Producto, Sucursal, Vendedor
from django.db.models import Q # Para búsquedas OR
from django.contrib.auth.decorators import login_required # Para el perfil
from django.contrib.auth.forms import UserChangeForm # Para modificar usuario base de Django
from django.contrib.auth.models import User # Para el modelo de usuario base
from .forms import (
    ClienteForm, ProductoForm, SucursalForm, VendedorForm, BusquedaForm,
    CustomUserCreationForm, PerfilUsuarioForm, UserEditForm
)
from .models import Cliente, Producto, Sucursal, Vendedor, PerfilUsuario

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

def registro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Cuenta creada para {user.username}. ¡Ya puedes iniciar sesión!")
            login(request, user) # Opcional: Iniciar sesión automáticamente después del registro
            return redirect('home')
        else:
            messages.error(request, "Error al registrar el usuario. Por favor, revisa los datos.")
    else:
        form = CustomUserCreationForm()
    return render(request, "myapp/registro.html", {"form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Has iniciado sesión como {username}.")
                return redirect('home')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    form = AuthenticationForm()
    return render(request, "myapp/login.html", {"form": form})

@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('home')

@login_required
def perfil_usuario(request):
    user_form = UserEditForm(instance=request.user)
    perfil_form = PerfilUsuarioForm(instance=request.user.perfilusuario)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=request.user.perfilusuario)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente!')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, revisa los datos.')

    return render(request, 'myapp/perfil_usuario.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

# Vista para ver el perfil de otro usuario (opcional)
def ver_perfil(request, username):
    usuario_a_ver = get_object_or_404(User, username=username)
    return render(request, 'myapp/ver_perfil.html', {'usuario': usuario_a_ver})

def lista_productos_por_cliente(request):
    # Obtener usuarios que han publicado al menos un producto
    # .distinct() es importante para evitar duplicados si un usuario tiene muchos productos
    usuarios_con_productos = User.objects.filter(productos_publicados__isnull=False).distinct()
    return render(request, 'myapp/lista_productos_por_cliente.html', {'usuarios_con_productos': usuarios_con_productos})

def lista_sucursales(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'myapp/lista_sucursales.html', {'sucursales': sucursales})

@login_required # Solo usuarios logueados pueden crear productos
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) # IMPORTANTE: request.FILES para la imagen
        if form.is_valid():
            producto = form.save(commit=False)
            producto.autor = request.user # Asigna el usuario logueado como autor
            producto.save()
            messages.success(request, 'Producto publicado con éxito!')
            return redirect('detalle_producto', pk=producto.pk) # Redirige al detalle
    else:
        form = ProductoForm()
    return render(request, 'myapp/form_producto.html', {'form': form, 'titulo': 'Publicar Producto'})

def lista_productos(request):
    productos = Producto.objects.all().order_by('-fecha_publicacion') # Los más nuevos primero
    return render(request, 'myapp/lista_productos.html', {'productos': productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'myapp/detalle_producto.html', {'producto': producto})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    # Verificar si el usuario logueado es el autor del producto
    if request.user != producto.autor:
        messages.error(request, 'No tienes permiso para editar este producto.')
        return redirect('detalle_producto', pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito!')
            return redirect('detalle_producto', pk=pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'myapp/form_producto.html', {'form': form, 'titulo': 'Editar Producto'})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    # Verificar si el usuario logueado es el autor del producto
    if request.user != producto.autor:
        messages.error(request, 'No tienes permiso para eliminar este producto.')
        return redirect('detalle_producto', pk=pk)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('home') # O a la lista de productos
    return render(request, 'myapp/confirm_delete.html', {'objeto': producto})

def lista_productos_por_cliente(request):
    # Obtener usuarios que han publicado al menos un producto
    usuarios_con_productos = User.objects.filter(productos_publicados__isnull=False).distinct()
    return render(request, 'myapp/lista_productos_por_cliente.html', {'usuarios_con_productos': usuarios_con_productos})