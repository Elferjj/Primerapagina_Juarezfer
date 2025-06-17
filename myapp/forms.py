from django import forms
from .models import Cliente, Producto, Sucursal, Vendedor

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