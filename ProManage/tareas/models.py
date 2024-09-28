from django.db import models
from Proyectos.models import Proyecto
from Usuarios.models import Usuario

# Create your models here.


class Tarea(models.Model):
    id_tarea = models.AutoField(primary_key=True)
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    id_asig_t = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tareas_asignadas')
    id_estado = models.ForeignKey('Proyectos.Estado', on_delete=models.CASCADE)


    def __str__(self):
        return self.descripcion
    

class TareaAsignacion(models.Model):
    id_asig_t = models.AutoField(primary_key=True)
    id_tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_usuario} - {self.id_tarea}"
    


class Entregable(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    url = models.URLField()
    id_tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entregable : {self.descripcion}"
    


class Archivo(models.Model):
    id_archivo = models.AutoField(primary_key=True)   
    nombre = models.CharField(max_length=100) 
    tamano = models.IntegerField()
    tipo = models.CharField(max_length=50)
    id_entrega = models.ForeignKey(Entregable, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre