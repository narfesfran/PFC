from django import forms
from django.forms import TextInput
from .models import Profile, Place, Photo, Favoritos, Votos


# -------------------------------------------------------------------------------
# FORMULARIO perfil de usuario
# -------------------------------------------------------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nombre', 'apellidos', 'correo', 'cat_preferidas', 'css')
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'Introduce el nombre', 'size': '35'}),
            'apellidos': TextInput(attrs={'placeholder': 'Introduce los apellidos', 'size': '35'}),
            'correo': TextInput(attrs={'placeholder': 'Introduce el correo electrónico', 'size': '35'})
        }
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'correo': 'email',
            'cat_preferidas': 'Preferencias',
            'css': 'Elegir estilo de la web'
        }

# -------------------------------------------------------------------------------
# FORMULARIO lugar
# -------------------------------------------------------------------------------
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('ref', 'tipo', 'name', 'description', 'image', 'categorias', 'latitude', 'longitude', 'url', 'rating')

# -------------------------------------------------------------------------------
# FORMULARIO marcar lugares favoritos
# -------------------------------------------------------------------------------
class FavoritosForm(forms.ModelForm):
    class Meta:
        model = Favoritos
        fields = ('usuario', 'lugar')

# -------------------------------------------------------------------------------
# FORMULARIO para votar lugares
# -------------------------------------------------------------------------------
class VotosForm(forms.ModelForm):
    class Meta:
        model = Votos
        fields = ('usuario', 'lugar', 'valor')

# -------------------------------------------------------------------------------
# FORMULARIO para las fotografías asociadas a los lugares
# -------------------------------------------------------------------------------
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('place', 'image')


# -------------------------------------------------------------------------------
# FORMULARIO para averiguar las coordenadas de una dirección
# -------------------------------------------------------------------------------
class AddressForm(forms.Form):
    address = forms.CharField(max_length=100, label="Localidad", required=True)

# -------------------------------------------------------------------------------
# FORMULARIO para establecer la posición del dispositivo vía IP
# -------------------------------------------------------------------------------
class LatLonForm(forms.Form):
    lat = forms.DecimalField(label='latitud', required=True)
    lon = forms.DecimalField(label='longitud', required=True)


