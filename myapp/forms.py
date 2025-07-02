from django import forms
from .models import Cliente, Producto, Sucursal, Vendedor
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Submit, Field

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
        fields = ['nombre', 'descripcion', 'precio','imagen'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock disponible'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}), 
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
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone_number',)

    def save(self, commit=True):
        
        user = super().save(commit=False) 

    
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save() 

            
            if self.cleaned_data['phone_number']:
                
                user.perfilusuario.telefono = self.cleaned_data['phone_number']
                user.perfilusuario.save()

        return user



class UserEditForm(UserChangeForm):
    password = None 

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') 

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',) 


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ['username', 'email'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('email'),
            Field('password'), 
            Field('password2'), 
            Submit('submit', 'Registrarse', css_class='btn btn-success mt-3')
        )

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    
    avatar = forms.ImageField(required=False) 

    class Meta:
        model = Profile
        fields = ['avatar'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('avatar'),
            
            Submit('submit', 'Actualizar Perfil', css_class='btn btn-primary mt-3')
        )

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] 
        


class ProfileUpdateForm(forms.ModelForm):
    

    class Meta:
        model = Profile
        fields = ['avatar', 'descripcion', 'telefono', 'link_web'] 
        
