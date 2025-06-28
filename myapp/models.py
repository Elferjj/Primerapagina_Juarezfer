from django.db import models
from django.contrib.auth.models import User
#from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    fecha_publicacion = models.DateTimeField(auto_now_add=True, null=True, blank=True) 
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos_publicados')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle_producto', args=[str(self.id)])

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    link_web = models.URLField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True) # Lo añadimos aquí para el registro

    def __str__(self):
        return f'Perfil de {self.user.username}'

# Función para crear automáticamente un PerfilUsuario cuando se crea un User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
    instance.perfilusuario.save() # Asegura que se actualice si ya existe