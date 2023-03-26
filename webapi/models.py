from django.db import models

# Create your models here.
class TipoMascota(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
    
class Color(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion

class Incapacidad(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
    
class Genero(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
    
class Raza(models.Model):
    descripcion = models.CharField(max_length=200)
    id_tipo_mascota = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
    
class Owner(models.Model):
    id_nacional = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    email = models.EmailField()
    id_genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.apellido
    
class Mascota(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    is_hembra = models.BooleanField()
    id_raza = models.ForeignKey(Raza, on_delete=models.CASCADE)
    id_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class MascotaColores(models.Model):
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    id_color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_mascota.nombre + " " + self.id_color.descripcion
    
class MascotaIncapacidad(models.Model):
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    id_incapacidad = models.ForeignKey(Incapacidad, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=500)
    fecha = models.DateField()

    def __str__(self):
        return self.id_mascota.nombre + " " + self.id_incapacidad.descripcion
    

