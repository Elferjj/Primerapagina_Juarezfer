Primerapagina_Juarezfer
Este proyecto es una aplicación web desarrollada con el framework Django, diseñada para explorar las funcionalidades básicas de un sistema de gestión de usuarios, productos y sucursales.

Cómo Empezar
Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

1. Clona el Repositorio
Si aún no tienes el código fuente, clónalo desde tu repositorio (o simplemente asegúrate de tener todos los archivos del proyecto).


git clone <url_de_tu_repositorio>
cd Primerapagina_Juarezfer


2. Configura el Entorno Virtual
Es una buena práctica usar entornos virtuales para aislar las dependencias de tu proyecto.

python -m venv .venv

3. Activa el Entorno Virtual
En Windows:


.venv\Scripts\activate
En macOS/Linux:


source .venv/bin/activate

4. Instala las Dependencias
Instala todas las librerías necesarias para el proyecto. Asegúrate de tener un archivo requirements.txt con todas las dependencias (como Django, Pillow, django-crispy-forms, etc.). Si no lo tienes, puedes instalar Django directamente:


pip install Django Pillow django-crispy-forms # y cualquier otra que necesites
(Idealmente, deberías tener un requirements.txt para esto: pip install -r requirements.txt)

5. Configura la Base de Datos
Django usa una base de datos SQLite por defecto, que es perfecta para desarrollo. Necesitas crear la estructura de la base de datos a partir de tus modelos.


python manage.py makemigrations myapp # Genera los archivos de migración para tu app
python manage.py migrate             # Aplica las migraciones a la base de datos


6. Crea un Superusuario (Opcional, pero recomendado)
Para acceder al panel de administración de Django, necesitarás un superusuario.



python manage.py createsuperuser
Sigue las instrucciones en pantalla para crear tu usuario administrador.

7. Ejecuta el Servidor de Desarrollo
Ahora puedes iniciar el servidor de desarrollo de Django.


python manage.py runserver
Una vez que el servidor esté en funcionamiento, abre tu navegador web y visita http://127.0.0.1:8000/ para ver la aplicación.

Estructura del Proyecto (Básica)

myproject/: Carpeta principal del proyecto, contiene la configuración global (settings.py, urls.py).

myapp/: Tu aplicación principal, contiene los modelos (models.py), vistas (views.py), formularios (forms.py), URLs de la aplicación (urls.py) y plantillas (templates/).

media/: Directorio para los archivos subidos por los usuarios (ej. avatares, imágenes de productos).

static/: Directorio para los archivos estáticos de tu aplicación (CSS, JavaScript, imágenes).

Video del proyecto 

https://youtu.be/9Miwc2oQpzk