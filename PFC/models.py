from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import URLField, CASCADE
from multiselectfield import MultiSelectField
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)


# -------------------------------------------------------------------------------
# MODELO perfil de usuario
# -------------------------------------------------------------------------------
class Profile(models.Model):
    Administradores = 'administradores'
    Usuarios = 'usuarios'
    TIPOS = (
        (Administradores, 'Administrador'),
        (Usuarios, 'Usuario'),
    )
    CAT0 = 0
    CAT1 = 1
    CAT2 = 2
    CAT3 = 3
    CAT4 = 4
    CAT5 = 5
    CAT6 = 6
    CAT7 = 7
    CAT8 = 8
    CATS = (
        (CAT0, 'Arte y Diseño'),
        (CAT1, 'Arquitectura'),
        (CAT2, 'Historia'),
        (CAT3, 'Ciencia y Tecnología'),
        (CAT4, 'Naturaleza'),
        (CAT5, 'Aventura'),
        (CAT6, 'Literatura'),
        (CAT7, 'Música'),
        (CAT8, 'Vida urbana'),
    )
    CLARO = '1'
    OSCURO = '2'
    SIMPLE = '3'
    CSS = (
        (CLARO, 'CLARO'),
        (OSCURO, 'OSCURO'),
        (SIMPLE, 'SIMPLE'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name='Rol')
    nombre = models.CharField(max_length=25, verbose_name='Nombre', null=True, blank=True)
    apellidos = models.CharField(max_length=35, verbose_name='Apellidos', null=True, blank=True)
    correo = models.EmailField(verbose_name='Correo electrónico', null=True, blank=True)
    cat_preferidas = MultiSelectField(choices=CATS, max_choices=9, verbose_name='Categorías', null=True, blank=True)
    css = models.CharField(max_length=1, choices=CSS, default=CLARO, verbose_name='Estilo de la web')

    def __str__(self):
        return self.user.username

# -------------------------------------------------------------------------------
# MODELO lugar
# -------------------------------------------------------------------------------
class Place(models.Model):
    CAT0 = 0
    CAT1 = 1
    CAT2 = 2
    CAT3 = 3
    CAT4 = 4
    CAT5 = 5
    CAT6 = 6
    CAT7 = 7
    CAT8 = 8
    CATS = (
        (CAT0, 'Arte y Diseño'),
        (CAT1, 'Arquitectura'),
        (CAT2, 'Historia'),
        (CAT3, 'Ciencia y Tecnología'),
        (CAT4, 'Naturaleza'),
        (CAT5, 'Aventura'),
        (CAT6, 'Literatura'),
        (CAT7, 'Música'),
        (CAT8, 'Vida urbana'),
    )
    tipos = (
        ('site', 'Sitio'),
        ('poi', 'Punto de Interés'),
    )
    ref = models.ForeignKey('Place', on_delete=CASCADE, blank=True, null=True)
    tipo = models.CharField(choices=tipos, max_length=4)
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(verbose_name='Imagen de portada')
    latitude = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='Latitud', validators=[MaxValueValidator(90.0), MinValueValidator(-90.0)])
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Longitud', validators=[MaxValueValidator(180.0), MinValueValidator(-180.0)])
    categorias = MultiSelectField(choices=CATS, max_choices=9, verbose_name='Categorías')
    url = URLField(verbose_name='URL')
    rating = models.IntegerField(verbose_name='Puntuación media', validators=[MaxValueValidator(100), MinValueValidator(0)])
    votes = models.IntegerField(verbose_name='Número de votos')
    likes = models.IntegerField(verbose_name='Número de veces favorito', null=True, blank=True)
    author = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def nota(self):
        resultado = self.rating / 10
        return resultado

    class Meta:
        ordering = ['name']

# -------------------------------------------------------------------------------
# MODELO fotografías asociadas a los lugares
# -------------------------------------------------------------------------------
class Photo(models.Model):
    place = models.ForeignKey(Place, verbose_name='Lugar de referencia')
    image = models.ImageField(verbose_name='Imagen')
    # thumbnail = models.CharField(max_length=200)

    def __str__(self):
        return self.place_id


# -------------------------------------------------------------------------------
# MODELO para establecer lugares favoritos
# -------------------------------------------------------------------------------
class Favoritos(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True)
    lugar = models.ForeignKey(Place, null=True, blank=True)

# -------------------------------------------------------------------------------
# MODELO para votar lugares
# -------------------------------------------------------------------------------
class Votos(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True)
    lugar = models.ForeignKey(Place, null=True, blank=True)
    valor = models.IntegerField(verbose_name='Puntuación media inicial', validators=[MaxValueValidator(100), MinValueValidator(0)])
