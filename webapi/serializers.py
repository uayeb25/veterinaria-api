from rest_framework import serializers
from webapi.models import TipoMascota, Color, Incapacidad, Genero, Raza, Owner, Mascota, MascotaColores, MascotaIncapacidad

class TipoMascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMascota
        fields = ('id', 'descripcion')

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'descripcion')

class IncapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incapacidad
        fields = ('id', 'descripcion')

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ('id', 'descripcion')

class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = ('id', 'descripcion', 'id_tipo_mascota')

class OwnerSerializer(serializers.ModelSerializer):
    def validate_id(self, value):
        # Verifica si ya existe un registro con este id en la base de datos
        if Owner.objects.filter(id=value).exists():
            raise serializers.ValidationError('Ya existe un owner con este id')
        return value
    
    class Meta:
        model = Owner
        fields = ('id', 'id_nacional','nombre', 'apellido', 'direccion', 'telefono', 'fecha_nacimiento', 'email', 'id_genero')

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = ('id', 'nombre', 'fecha_nacimiento', 'is_hembra', 'id_raza', 'id_owner')

class MascotaColoresSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='id_color.descripcion', read_only=True)    
    class Meta:
        model = MascotaColores
        fields = ('id', 'id_mascota', 'id_color', 'color')

class MascotaIncapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MascotaIncapacidad
        fields = ('id', 'id_mascota', 'id_incapacidad', 'descripcion')

