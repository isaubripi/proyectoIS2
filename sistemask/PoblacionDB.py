from adm_proyectos.models import Cliente
from adm_flujos.models import Flujo
from adm_actividades.models import Actividad
from adm_historias.models import Historia, Historial
from adm_proyectos.models import Proyecto
from adm_usuarios.models import Usuario
from adm_roles.models import Rol
from adm_sprints.models import Sprint

#primero se crearan los roles del sistema
scrum_master = Rol(nombre='Scrum Master', 
		crear_proyecto =True, 
    		modificar_proyecto = True,
    		eliminar_proyecto = True,
    		cerrar_proyecto = True,

    		crear_usuario = True,
    		modificar_usuario = True,
    		eliminar_usuario = True,
    		agregar_rol = True,
    		modificar_rol = True,
    		eliminar_rol = True,

    		generar_resumen_clientes = True,
	    	generar_burndown = True,

	    	asignar_usuario_inicial = True,
	    	asignar_permisos_roles = True,
	    	asignar_roles_usuario = True,
	    	asignar_usuarios_proyecto = True,

	    	listar_usuarios = True,
	    	listar_proyectos =True,

	    	agregar_sprint = True,
	    	modificar_sprint = True,
	    	eliminar_sprint = True,
	    	activar_sprint = True,

	    	agregar_historia = True,
	    	modificar_historia = True,
	    	eliminar_historia = True,
	    	adjuntar_archivos = True,
	    	cargar_horas = True,
	    	actualizar_estado = True,
	    	ver_historial = True,
	    	validar_historia = True,

	    	crear_flujo = True,
	    	modificar_flujo = True,
	    	eliminar_flujo = True,
	    	ver_tabla = True,
)

scrum_master.save()
#se crean 2 usuarios con el rol scrum_master

isidro = Usuario(username='isidro', nombre='Isidro', apellido='Brizuela', password='isidro', cedula='3841270', email='isidro@gmail.com', estado=True)
isidro.save()
isidro.roles.add(scrum_master)
isidro.save()

ruben = Usuario(username='ruben', nombre='Ruben', apellido='Medina', password='ruben', cedula='5', email='ruben@gmail.com', estado=True)
ruben.save()
ruben.roles.add(scrum_master)
ruben.save()

#se crea un cliente
cliente1 = Cliente(username='tigo', nombre='Victor', apellido='Vazquez', password='tigo', cedula='333', email='tigo@gmail.com', estado=True)
cliente1.save()
#se crea un proyecto

Proyecto1 = Proyecto(nombre='Proyecto1', descripcion='Escrito en python', scrum_master = isidro, fecha_inicio='2015-05-01', fecha_fin='2015-06-01', activo=True, cliente=cliente1)
Proyecto1.save()
Proyecto1.scrum_team.add(isidro)
Proyecto1.scrum_team.add(ruben)
Proyecto1.save()

#se crea un flujo para el proyecto
flujo1 = Flujo(nombre='Flujo1', proyecto=Proyecto1, descripcion='Desarrollo de SW', activo=True, nro_actividades=2)
flujo1.save()

#se crean actividades para el flujo
actividad1 = Actividad(nombre='Analisis', proyecto=Proyecto1,descripcion='Analisis', flujo=flujo1.id, secuencia=1, estado=True, asignado_h=False)
actividad1.save()

actividad2 = Actividad(nombre='Disenho', proyecto=Proyecto1,descripcion='Disenho', flujo=flujo1.id, secuencia=2, estado=True, asignado_h=False)
actividad2.save()

flujo1.actividades.add(actividad1)
flujo1.actividades.add(actividad2)
flujo1.save()

#se crea un sprint
sprint1 = Sprint(nombre='Sprint1', descripcion='Fase inicial', fecha_inicio='2015-05-01', fecha_fin='2015-06-01', duracion=30, proyecto=Proyecto1, activo=True, estado='A', asignado_h=True)
sprint1.save()

#se crean historias 
historia1 = Historia(nombre='Historia1', proyecto=Proyecto1, prioridad=1, val_negocio=1, val_tecnico=1, size=10, descripcion='Hacer Login', codigo='001', acumulador=0, asignado=ruben, flujo=flujo1, estado='Doing', actividad=actividad1, sprint=sprint1.id, asignado_p=True, activo=True)
historia1.save()

historia2 = Historia(nombre='Historia2', proyecto=Proyecto1, prioridad=1, val_negocio=1, val_tecnico=1, size=10, descripcion='Hacer Logout', codigo='002', acumulador=0, asignado=ruben, flujo=flujo1, estado='Doing', actividad=actividad2, sprint=sprint1.id, asignado_p=True, activo=True)
historia2.save()

sprint1.historias.add(historia1)
sprint1.historias.add(historia2)
sprint1.save()

historial1 = Historial(id_historia=historia1, nombre='Historia1', proyecto=Proyecto1, prioridad=1, val_negocio=1, val_tecnico=1, size=10, descripcion='Hacer Login', codigo='001', acumulador=0, asignado=ruben, flujo=flujo1, estado='Doing', actividad=actividad1, sprint=sprint1.id, asignado_p=True, activo=True, fecha='2015-05-01')
historial1.save()

historial2 = Historial(id_historia=historia2, nombre='Historia2', proyecto=Proyecto1, prioridad=1, val_negocio=1, val_tecnico=1, size=10, descripcion='Hacer Login', codigo='001', acumulador=0, asignado=ruben, flujo=flujo1, estado='Doing', actividad=actividad2, sprint=sprint1.id, asignado_p=True, activo=True, fecha='2015-05-01')
historial2.save()





