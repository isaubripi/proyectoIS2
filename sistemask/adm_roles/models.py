from django.db import models
from adm_usuarios.models import Usuario


class Rol(models.Model):

    nombre = models.CharField(max_length=50)


    #Administracion de Proyectos

    crear_proyecto = models.BooleanField(default=False)
    modificar_proyecto = models.BooleanField(default=False)
    eliminar_proyecto = models.BooleanField(default=False)
    cerrar_proyecto = models.BooleanField(default=False)

    #Administracion de Usuarios

    crear_usuario = models.BooleanField(default=False)
    modificar_usuario = models.BooleanField(default=False)
    eliminar_usuario = models.BooleanField(default=False)

    #Administracion de Roles

    agregar_rol = models.BooleanField(default=False)
    modificar_rol = models.BooleanField(default=False)
    eliminar_rol = models.BooleanField(default=False)

    #Generar resumen de clientes y burndown chart


    generar_resumen_clientes = models.BooleanField(default=False)
    generar_burndown = models.BooleanField(default=False)

    #Asignacion

    asignar_usuario_inicial = models.BooleanField(default=False)
    asignar_permisos_roles = models.BooleanField(default=False)
    asignar_roles_usuario = models.BooleanField(default=False)
    asignar_usuarios_proyecto = models.BooleanField(default=False)

    #Listar

    listar_usuarios = models.BooleanField(default=False)
    listar_proyectos = models.BooleanField(default=False)

    #Administracion de Sprints

    agregar_sprint = models.BooleanField(default=False)
    modificar_sprint = models.BooleanField(default=False)
    eliminar_sprint = models.BooleanField(default=False)
    activar_sprint = models.BooleanField(default=False)

    #Administracion de User Stories

    agregar_historia = models.BooleanField(default=False)
    modificar_historia = models.BooleanField(default=False)
    eliminar_historia = models.BooleanField(default=False)
    adjuntar_archivos = models.BooleanField(default=False)
    cargar_horas = models.BooleanField(default=False)
    actualizar_estado = models.BooleanField(default=False)
    ver_historial = models.BooleanField(default=False)
    validar_historia = models.BooleanField(default=False)

    #Administracion de Tabla kanban

    crear_flujo = models.BooleanField(default=False)
    modificar_flujo = models.BooleanField(default=False)
    eliminar_flujo = models.BooleanField(default=False)
    ver_tabla = models.BooleanField(default=False)

    activo = models.BooleanField(default=False)
    usuario= models.ForeignKey(Usuario)

    def __unicode__(self):
        return self.nombre



