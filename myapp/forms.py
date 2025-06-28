from django import forms
from .models import Cliente, Producto, Sucursal, Vendedor
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del cliente'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock disponible'}),
        }

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sucursal'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de la sucursal'}),
        }

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nombre', 'apellido', 'codigo_empleado', 'sucursal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del vendedor'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del vendedor'}),
            'codigo_empleado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único de empleado'}),
            'sucursal': forms.Select(attrs={'class': 'form-control'}), # Django creará un select para la FK
        }

class BusquedaForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre...'}))
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    first_name = forms.CharField(label="Nombre", max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}))
    last_name = forms.CharField(label="Apellido", max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'}))
    phone_number = forms.CharField(label="Número de teléfono", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +5491112345678'}))

    class Meta(UserCreationForm.Meta):
        model = User # Usaremos el modelo User por defecto de Django
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone_number',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email'] # Guardamos el email
        if commit:
            user.save()
            # Creamos el perfil de usuario extendido
            perfil = PerfilUsuario.objects.create(user=user, telefono=self.cleaned_data['phone_number'])
            perfil.save()
        return user


# Para modificar los campos extra del perfil
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['descripcion', 'link_web', 'avatar', 'telefono']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuentanos un poco sobre ti...'}),
            'link_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ej: https://tupagina.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}), # Para subir archivos
        }

# Para modificar los campos base del usuario (nombre, apellido, email)
class UserEditForm(UserChangeForm):
    password = None # No queremos que la contraseña se muestre o sea editable aquí

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

