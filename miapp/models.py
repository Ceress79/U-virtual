from django.dispatch import receiver
import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_delete
from django.utils import timezone

class asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creditos = models.IntegerField()
    curso = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
    
    def __str__(self):
        return self.nombre

# Modelo Usuario personalizado
class UserManager(BaseUserManager):
    def create_user(self, dni, first_name, last_name, password=None, **extra_fields):
        if not dni:
            raise ValueError('jijiji ja aña')
        if not first_name or not last_name:
            raise ValueError('The given name and last name must be set')
        user = self.model(
            dni=dni,
            first_name=first_name.strip().upper(),
            last_name=last_name.strip().upper(),
            username=f"{first_name} {last_name}",
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(dni, first_name, last_name, password, **extra_fields)


def obtener_ruta_subida(instance, filename):
    ruta = instance.dni.strip()
    return os.path.join('profile', ruta, filename)
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=obtener_ruta_subida, blank=True, null=True)
    date_born = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    roles = [
        ('docente', 'Docente'),
        ('administrativo', 'Personal Administrativo'),
        ('estudiante', 'Estudiante')
    ]
    rol = models.CharField(max_length=15, choices=roles)
    asignatura = models.ForeignKey(asignatura, related_name='usuarios', on_delete=models.SET_NULL, null=True, blank=True)

    EMAIL_FIELD = 'email'   
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    USERNAME_FIELD = 'dni'
    
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['dni', 'rol']

@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.profile_picture and instance.profile_picture.name != 'default.png':
        # Obtén la ruta del archivo de imagen
        image_path = instance.profile_picture.path
        # Elimina el archivo de imagen si existe
        if os.path.isfile(image_path):
            os.remove(image_path)
        # Obtén el directorio que contiene la imagen
        directory = os.path.dirname(image_path)
        # Intenta eliminar el directorio si está vacío
        try:
            os.rmdir(directory)
        except OSError:
            pass  # El directorio no está vacío o no se pudo eliminar


class actividad(models.Model):
    asignatura = models.ForeignKey(asignatura, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada')
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"{self.nombre}"


class calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    asignatura = models.ForeignKey(asignatura, on_delete=models.CASCADE, null=True)
    actividad = models.ForeignKey(actividad, on_delete=models.CASCADE, null=True)
    nota = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_entrega = models.DateField(null=True, blank=True)
    comentario = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.actividad} - {self.nota}"
    
    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"


class horario(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    asignatura = models.ForeignKey(asignatura, on_delete=models.CASCADE, null=True)
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin}"