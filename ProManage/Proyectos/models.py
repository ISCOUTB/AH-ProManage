from django.db import models
from Usuarios.models import Usuario

# Create your models here.
class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)

    def __str__(self) :
        return self.estado
    

class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    id_asig = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos_asignados')
    id_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    

class ProyectoAsignacion(models.Model):
    id_asig = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_usuario} - {self.id_proyecto}"