from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from django.contrib import messages 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Cliente, Producto, Sucursal, Vendedor
from django.db.models import Q 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserChangeForm 
from django.contrib.auth.models import User 
from .forms import (
    ClienteForm, ProductoForm, SucursalForm, VendedorForm, BusquedaForm,
    CustomUserCreationForm, UserEditForm,ProfileEditForm
)
from .models import Profile
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from .forms import UserRegisterForm
from .forms import UserUpdateForm, ProfileUpdateForm


def home(request):
    return render(request, 'myapp/home.html')





def about(request):
    context = {
        'creador_nombre': 'Juarez Fernando Gabriel',
        'creador_profesion': 'Policía de la Provincia de Buenos Aires',
        'dedicacion_curso': 'dedicó mucho tiempo y dedicación al curso.',
        'objetivo_web': 'Básicamente quería crear una web donde personas puedan encontrarse en una sucursal de videojuegos y poder hacer ventas de sus productos electrónicos.'
    }
    
    return render(request, 'myapp/about.html', context)

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save() 
                messages.success(request, f'Cuenta creada exitosamente para {user.username}!')
                return redirect('login')
            except IntegrityError:
                
                messages.error(request, 'Error al registrar el usuario. El nombre de usuario o correo electrónico ya podría estar en uso.')
                
        else:
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
            

    else: 
        form = UserRegisterForm()

    return render(request, 'myapp/register.html', {'form': form})
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
                return redirect('inicio')
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
    return redirect('inicio')

@login_required 
def edit_profile(request):
    
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile) 

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('edit_profile') 
        else:
            messages.error(request, 'Hubo un error al actualizar tu perfil.')
            print("Errores UserForm:", user_form.errors) 
            print("Errores ProfileForm:", profile_form.errors) 
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'myapp/edit_profile.html', context)


def ver_perfil_usuario(request, username):
    usuario_a_ver = get_object_or_404(User, username=username)
    es_propio_perfil = (request.user == usuario_a_ver)

    user_form = None
    perfil_form = None

    if es_propio_perfil:
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            perfil_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and perfil_form.is_valid():
                user_form.save()
                perfil_form.save()
                # Añadir un mensaje de éxito
                from django.contrib import messages
                messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
                return redirect('ver_perfil_usuario', username=request.user.username)
        else:
            user_form = UserUpdateForm(instance=request.user)
            perfil_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'usuario': usuario_a_ver, # El usuario cuyo perfil estamos viendo
        'es_propio_perfil': es_propio_perfil,
        'user_form': user_form,
        'perfil_form': perfil_form,
    }
    return render(request, 'myapp/perfil_usuario.html', context)


def lista_productos_por_cliente(request):
    
    usuarios_con_productos = User.objects.filter(productos_publicados__isnull=False).distinct()
    return render(request, 'myapp/lista_productos_por_cliente.html', {'usuarios_con_productos': usuarios_con_productos})

def lista_sucursales(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'myapp/lista_sucursales.html', {'sucursales': sucursales})



@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES) 
        if form.is_valid():
            producto = form.save(commit=False)
            producto.autor = request.user
            producto.save()
            messages.success(request, 'Producto publicado exitosamente.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al publicar el producto. Revisa los campos.')
    else:
        form = ProductoForm() 
        print("DEBUG: La vista crear_producto está a punto de renderizar la plantilla.") 

    
    return render(request, 'myapp/crear_producto.html', {'form': form})

def lista_productos(request):
    productos = Producto.objects.all().order_by('-fecha_publicacion') 
    return render(request, 'myapp/lista_productos.html', {'productos': productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'myapp/detalle_producto.html', {'producto': producto})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
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
    
    if request.user != producto.autor:
        messages.error(request, 'No tienes permiso para eliminar este producto.')
        return redirect('detalle_producto', pk=pk)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('home') 
    return render(request, 'myapp/confirm_delete.html', {'objeto': producto})

def lista_productos_por_cliente(request):
    
    usuarios_con_productos = User.objects.filter(productos_publicados__isnull=False).distinct()
    return render(request, 'myapp/lista_productos_por_cliente.html', {'usuarios_con_productos': usuarios_con_productos})

def lista_sucursales(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'myapp/lista_sucursales.html', {'sucursales': sucursales})

@login_required
def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False) 
            sucursal.creador = request.user    
            sucursal.save()                    
            messages.success(request, f'Sucursal "{sucursal.nombre}" creada exitosamente.')
            return redirect('lista_sucursales')
    else:
        form = SucursalForm()
    return render(request, 'myapp/crear_sucursal.html', {'form': form})



def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('nombre') 
    return render(request, 'myapp/lista_clientes.html', {'clientes': clientes})



@login_required
def perfil_usuario(request, username=None): 
    if username:
        
        user_to_view = get_object_or_404(User, username=username)
        
        
        if request.user == user_to_view:
            es_propio_perfil = True
        else:
            es_propio_perfil = False
    else:
        
        user_to_view = request.user
        es_propio_perfil = True

    perfil, created = PerfilUsuario.objects.get_or_create(user=user_to_view)
    productos_publicados = user_to_view.productos_publicados.all() 

    if es_propio_perfil: 
        if request.method == 'POST':
            user_form = UserEditForm(request.POST, instance=request.user)
            perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
            if user_form.is_valid() and perfil_form.is_valid():
                user_form.save()
                perfil_form.save()
                messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
                return redirect('perfil_usuario') 
            else:
                messages.error(request, 'Error al actualizar el perfil. Por favor, revisa los datos.')
        else:
            user_form = UserEditForm(instance=request.user)
            perfil_form = PerfilUsuarioForm(instance=perfil)
    else: 
        user_form = None
        perfil_form = None

    context = {
        'user_to_view': user_to_view,
        'perfil': perfil,
        'user_form': user_form,
        'perfil_form': perfil_form,
        'es_propio_perfil': es_propio_perfil,
        'productos_publicados': productos_publicados, 
    }
    return render(request, 'myapp/perfil_usuario.html', context)

@login_required
def eliminar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    
    if request.user == sucursal.creador:
        if request.method == 'POST': 
            sucursal.delete()
            messages.success(request, f'Sucursal "{sucursal.nombre}" eliminada exitosamente.')
            return redirect('lista_sucursales')
        
        messages.info(request, f'Confirma la eliminación de "{sucursal.nombre}".')
        return render(request, 'myapp/confirmar_eliminar_sucursal.html', {'sucursal': sucursal})
    else:
        messages.error(request, 'No tienes permiso para eliminar esta sucursal.')
        return redirect('lista_sucursales')
    

    
