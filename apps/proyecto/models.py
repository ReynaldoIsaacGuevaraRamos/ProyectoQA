from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Agencia(models.Model):
    codigo_agencia = models.CharField(primary_key=True, max_length=15, null=False)
    nombre_agencia = models.CharField(max_length=250, null=False)
    direccion_agencia = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.codigo_agencia


class Departamento(models.Model):
    codigo_departamento = models.CharField(primary_key=True, max_length=15, null=False)
    nombre_departamento = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.nombre_departamento


class Comite(models.Model):
    id_comite = models.AutoField(primary_key=True)
    nombre_comite = models.CharField(max_length=150, null=False, unique=True)
    descripcion_comite = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombre_comite


class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre_actividad = models.CharField(max_length=150, null=False)
    descripcion_actividad = models.CharField(max_length=250, null=True, blank=True)
    fecha_realizacion = models.DateField(auto_now=False, auto_now_add=False)
    codigo_agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    codigo_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_comite = models.ForeignKey(Comite, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_actividad.__str__()


class EncuestaCliente(models.Model):
    codigo_agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    descripcion_pregunta = models.CharField(max_length=300, null=False)
    titulo_encuesta_cliente = models.CharField(max_length=250, null=False)
    visibilidad_pregunta_cliente = models.CharField(max_length=1, null=False, default='S')
    fecha_desde_cliente = models.DateField(null=False)
    fecha_hasta_cliente = models.DateField(null=True, blank=True)

    #class Meta:
    #    unique_together = ("codigo_agencia", "id_pregunta")
    
    def __str__(self):
        return self.codigo_agencia.__str__() +' | '+ self.titulo_encuesta_cliente.__str__() +' | '+ self.descripcion_pregunta.__str__()


class RespuestaEncuestaCliente(models.Model):
    id_respuesta_encuesta_cliente = models.AutoField(primary_key=True)
    respuesta_cliente = models.IntegerField(null=False)
    encuesta = models.ForeignKey(EncuestaCliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.encuesta.__str__() + ' | ' + self.respuesta_cliente.__str__()


class EncuestaPersonal(models.Model):
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    descripcion_pregunta = models.CharField(max_length=300, null=False)
    titulo_encuesta_personal = models.CharField(max_length=250, null=False)
    visibilidad_pregunta_personal = models.CharField(max_length=1, null=False, default='S')
    fecha_desde_personal = models.DateField(null=False)
    fecha_hasta_personal = models.DateField(null=True, blank=True)

    #class Meta:
    #    unique_together = ("id_actividad", "id_pregunta")
    
    def __str__(self):
        return self.id_actividad.__str__() +' | '+ self.titulo_encuesta_personal.__str__() +' | '+ self.descripcion_pregunta.__str__()


class RespuestaEncuestaPersonal(models.Model):
    id_respuesta_encuesta_personal = models.AutoField(primary_key=True)
    respuesta_personal = models.IntegerField(null=False)
    encuesta = models.ForeignKey(EncuestaPersonal, on_delete=models.CASCADE)

    def __str__(self):
        return self.encuesta.__str__() + ' | ' + self.respuesta_personal.__str__()


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)    
    codigo_agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    codigo_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_comite = models.ForeignKey(Comite, on_delete=models.CASCADE)
    email = models.EmailField('Correo Electrónico', max_length=254,unique = True)
    nombres = models.CharField('Nombres', max_length=100, blank = False, null = False)
    apellidos = models.CharField('Apellidos', max_length=100,blank = False, null = False)
    
    def __str__(self):
        return self.nombres.__str__() + ' '+ self.apellidos.__str__()