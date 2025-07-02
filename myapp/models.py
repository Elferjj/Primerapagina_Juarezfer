from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver



class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos_publicados')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle_producto', args=[str(self.id)])


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sucursales_creadas')

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle_sucursal', args=[str(self.id)]) 

class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # O con related_name='profile' o 'perfilusuario'
    avatar = models.ImageField(default='default.png', upload_to='profile_pics') # Asegúrate de que exista y se llame 'avatar'
    descripcion = models.TextField(blank=True, null=True) # Asegúrate de que exista y se llame 'descripcion'
    telefono = models.CharField(max_length=20, blank=True, null=True) # Asegúrate de que exista y se llame 'telefono'
    link_web = models.URLField(blank=True, null=True) # Asegúrate de que exista y se llame 'link_web'

    def __str__(self):
        return f'{self.user.username} Profile'




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
         Profile.objects.create(user=instance)

   

