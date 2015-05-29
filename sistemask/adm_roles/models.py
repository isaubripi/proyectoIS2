from django.db import models
#from adm_proyectos.models import Proyecto
#from adm_usuarios.models import Usuario


class Rol(models.Model):
    '''
    Esta clase define el modelo Rol.
    Los campos de este modelo, ademas de todos los permisos del sistema, son:
        nombre: nombre del rol,
        activo: determina si el rol esta o no activo en el sistema.
    '''

    nombre = models.CharField(max_length=50)
    #proyecto = models.ForeignKey(Proyecto)

    #Administracion de Proyectos

    crear_proyecto = models.BooleanField(default=False)
    modificar_proyecto = models.BooleanField(default=False)
    eliminar_proyecto = models.BooleanField(default=False)
    cerrar_proyecto = models.BooleanField(default=False)
    inicializar_proyecto = models.BooleanField(default=False)
    ingresar_proyecto = models.BooleanField(default=False)

    #Administracion de Usuarios

    crear_usuario = models.BooleanField(default=False)
    modificar_usuario = models.BooleanField(default=False)
    eliminar_usuario = models.BooleanField(default=False)

    #Administracion de Roles

    agregar_rol = models.BooleanField(default=False)
    modificar_rol = models.BooleanField(default=False)
    eliminar_rol = models.BooleanField(default=False)

    #Generar resumen de clientes y burndown chart


    generar_reporte = models.BooleanField(default=False)
    generar_burndown = models.BooleanField(default=False)

    #Asignacion

    asignar_usuario_inicial = models.BooleanField(default=False)
    asignar_permisos_roles = models.BooleanField(default=False)
    asignar_roles_usuario = models.BooleanField(default=False)
    asignar_usuarios_proyecto = models.BooleanField(default=False)
    asignar_usuario_flujo = models.BooleanField(default=False)
    asignar_equipo = models.BooleanField(default=False)

    #Administracion de Sprints

    agregar_sprint = models.BooleanField(default=False)
    modificar_sprint = models.BooleanField(default=False)
    eliminar_sprint = models.BooleanField(default=False)
    activar_sprint = models.BooleanField(default=False)
    ver_sprintbacklog = models.BooleanField(default=False)

    #Administracion de User Stories

    agregar_historia = models.BooleanField(default=False)
    modificar_historia = models.BooleanField(default=False)
    eliminar_historia = models.BooleanField(default=False)
    cargar_horas = models.BooleanField(default=False)
    cambiar_actividad_estado = models.BooleanField(default=False)
    ver_historial = models.BooleanField(default=False)
    ver_detalles = models.BooleanField(default=False)
    cancelar_historia = models.BooleanField(default=False)
    asignar_historia = models.BooleanField(default=False)
    desasignar_historia = models.BooleanField(default=False)
    release_historia = models.BooleanField(default=False)
    finalizar_historia = models.BooleanField(default=False)
    horas_sprint = models.BooleanField(default=False)

    #Administracion de Tabla kanban

    crear_flujo = models.BooleanField(default=False)
    modificar_flujo = models.BooleanField(default=False)
    eliminar_flujo = models.BooleanField(default=False)
    ver_tabla = models.BooleanField(default=False)

    #Administracion de Actividades
    crear_actividad = models.BooleanField(default=False)
    modificar_actividad = models.BooleanField(default=False)
    eliminar_actividad = models.BooleanField(default=False)
    establecer_secuencia = models.BooleanField(default=False)
    restablecer_secuencia = models.BooleanField(default=False)

    activo = models.BooleanField(default=False)
    #usuario= models.ForeignKey(Usuario)

    def __unicode__(self):
        return self.nombre



