

from django.shortcuts import render

from adm_usuarios.models import Usuario
from django.views.generic import TemplateView
from .models import Rol

# Create your views here.
class RolView(TemplateView):
    '''Esta clase muestra la lista de roles.

    '''
    template_name = 'Rol.html'
    #context_object_name = 'lista_roles'
    def post(self, request, *args, **kwargs):
        #diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        #f len(Rol.objects.filter(nombre= 'Lider del Proyecto', usuario= usuario_logueado, proyecto= proyecto_actual)):
            #diccionario[self.context_object_name]= Rol.objects.filter(proyecto= proyecto_actual, activo= True)
        lista = Rol.objects.filter(activo = True)
        return render(request, self.template_name, {'lista':lista})
        #else:
         #   diccionario[super(RolView, self).context_object_name]= Fase.objects.filter(proyecto= proyecto_actual)
         #   diccionario['error']= 'No posee permisos para visualizar los roles del proyecto'
         #   return render(request, super(RolView, self).template_name, diccionario)

class CrearRol(RolView):

    template_name = 'CrearRol.html'
    def post(self, request, *args, **kwargs):
        #diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        lista = Usuario.objects.all()
        return render(request, self.template_name, {'lista_usuarios' : lista})

class CrearRolConfirm(CrearRol):
    template_name = 'CrearRolConfirm.html'
    def post(self, request, *args, **kwargs):
        #diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        rol_nombre= request.POST['nombre_rol']
        if len(Rol.objects.filter(nombre= rol_nombre, activo= True)):
            error = "Nombre del rol ya existe. Intente otro"
            return render(request, super(CrearRolConfirm, self).template_name, {'error':error})
        nuevo_rol = Rol(nombre= rol_nombre,usuario= Usuario.objects.get(username= request.POST['usuario_rol']))


        nuevo_rol.save()
        #Completamos los permisos
        if 'crear_proyecto' in request.POST: nuevo_rol.crear_proyecto= True
        if 'modificar_proyecto' in request.POST: nuevo_rol.modificar_proyecto= True
        if 'eliminar_proyecto' in request.POST: nuevo_rol.eliminar_proyecto= True
        if 'cerrar_proyecto' in request.POST: nuevo_rol.cerrar_proyecto= True
        if 'crear_usuario' in request.POST: nuevo_rol.crear_usuario= True
        if 'modificar_usuario' in request.POST: nuevo_rol.modificar_usuario= True
        if 'eliminar_usuario' in request.POST: nuevo_rol.eliminar_usuario= True
        if 'agregar_rol' in request.POST: nuevo_rol.agregar_rol= True
        if 'modificar_rol' in request.POST: nuevo_rol.modificar_rol= True
        if 'eliminar_rol' in request.POST: nuevo_rol.eliminar_rol= True
        if 'generar_resumen_clientes' in request.POST: nuevo_rol.generar_resumen_clientes= True
        if 'generar_burndown' in request.POST: nuevo_rol.generar_burndown= True
        if 'asignar_usuario_inicial' in request.POST: nuevo_rol.asignar_usuario_inicial= True
        if 'asignar_permisos_roles' in request.POST: nuevo_rol.asignar_permisos_roles= True
        if 'asignar_roles_usuario' in request.POST: nuevo_rol.asignar_roles_usuario= True
        if 'asignar_usuarios_proyecto' in request.POST: nuevo_rol.asignar_usuarios_proyecto= True
        if 'listar_usuarios' in request.POST: nuevo_rol.listar_usuarios= True
        if 'listar_proyectos' in request.POST: nuevo_rol.listar_proyectos= True
        if 'agregar_sprint' in request.POST: nuevo_rol.agregar_sprint= True
        if 'modificar_sprint' in request.POST: nuevo_rol.modificar_sprint= True
        if 'eliminar_sprint' in request.POST: nuevo_rol.eliminar_sprint= True
        if 'activar_sprint' in request.POST: nuevo_rol.activar_sprint= True
        if 'agregar_historia' in request.POST: nuevo_rol.agregar_historia= True
        if 'modificar_historia' in request.POST: nuevo_rol.modificar_historia= True
        if 'eliminar_historia' in request.POST: nuevo_rol.eliminar_historia= True
        if 'adjuntar_archivos' in request.POST: nuevo_rol.adjuntar_archivos= True
        if 'cargar_horas' in request.POST: nuevo_rol.cargar_horas= True
        if 'actualizar_estado' in request.POST: nuevo_rol.actualizar_estado= True
        if 'ver_historial' in request.POST: nuevo_rol.ver_historial= True
        if 'validar_historia' in request.POST: nuevo_rol.validar_historia= True
        if 'crear_flujo' in request.POST: nuevo_rol.crear_flujo= True
        if 'modificar_flujo' in request.POST: nuevo_rol.modificar_flujo= True
        if 'eliminar_flujo' in request.POST: nuevo_rol.eliminar_flujo= True
        if 'ver_tabla' in request.POST: nuevo_rol.ver_tabla= True
        nuevo_rol.activo= True

        nuevo_rol.save()
        return render(request, self.template_name)


class EditarRol(RolView):
    template_name = 'EditarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        if rol_actual.nombre== 'Scrum Master':
            error = 'Rol: Scrum Master - No se puede modificar'
            #diccionario[super(EditarRol, self).context_object_name]= Rol.objects.filter(proyecto= proyecto_actual, activo= True)
            return render(request, super(EditarRol, self).template_name, {'error':error})
        diccionario['rol']= rol_actual
        return render(request, self.template_name, diccionario)

class EditarRolConfirmar(EditarRol):
    template_name = 'EditarRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        roles= Rol.objects.filter(nombre= request.POST['nombre_rol'])
        nuevo_rol_nombre= request.POST['nombre_nuevo_rol']
        #Actualizamos los permisos
        for rol_actual in roles:
            rol_actual.nombre= nuevo_rol_nombre
            if 'crear_proyecto' in request.POST: rol_actual.crear_proyecto= True
            else: rol_actual.crear_proyecto= False
            if 'modificar_proyecto' in request.POST: rol_actual.modificar_proyecto= True
            else: rol_actual.modificar_proyecto= False
            if 'eliminar_proyecto' in request.POST: rol_actual.eliminar_proyecto= True
            else: rol_actual.eliminar_proyecto= False
            if 'cerrar_proyecto' in request.POST: rol_actual.cerrar_proyecto= True
            else: rol_actual.cerrar_proyecto= False
            if 'crear_usuario' in request.POST: rol_actual.crear_usuario= True
            else: rol_actual.crear_usuario= False
            if 'modificar_usuario' in request.POST: rol_actual.modificar_usuario= True
            else: rol_actual.modificar_usuario= False
            if 'eliminar_usuario' in request.POST: rol_actual.eliminar_usuario= True
            else: rol_actual.eliminar_usuario= False
            if 'agregar_rol' in request.POST: rol_actual.agregar_rol= True
            else: rol_actual.agregar_rol= False
            if 'modificar_rol' in request.POST: rol_actual.modificar_rol= True
            else: rol_actual.modificar_rol= False
            if 'eliminar_rol' in request.POST: rol_actual.eliminar_rol= True
            else: rol_actual.eliminar_rol= False
            if 'generar_resumen_clientes' in request.POST: rol_actual.generar_resumen_clientes= True
            else: rol_actual.generar_resumen_clientes= False
            if 'generar_burndown' in request.POST: rol_actual.generar_burndown= True
            else: rol_actual.generar_burndown= False
            if 'asignar_usuario_inicial' in request.POST: rol_actual.asignar_usuario_inicial= True
            else: rol_actual.asignar_usuario_inicial= False
            if 'asignar_permisos_roles' in request.POST: rol_actual.asignar_permisos_roles= True
            else: rol_actual.asignar_permisos_roles= False
            if 'asignar_roles_usuario' in request.POST: rol_actual.asignar_roles_usuario= True
            else: rol_actual.asignar_roles_usuario= False
            if 'asignar_usuarios_proyecto' in request.POST: rol_actual.asignar_usuarios_proyecto= True
            else: rol_actual.asignar_usuarios_proyecto= False
            if 'listar_usuarios' in request.POST: rol_actual.listar_usuarios= True
            else: rol_actual.listar_usuarios= False
            if 'listar_proyectos' in request.POST: rol_actual.listar_proyectos= True
            else: rol_actual.listar_proyectos= False
            if 'agregar_sprint' in request.POST: rol_actual.agregar_sprint= True
            else: rol_actual.agregar_sprint= False
            if 'modificar_sprint' in request.POST: rol_actual.modificar_sprint= True
            else: rol_actual.modificar_sprint= False
            if 'eliminar_sprint' in request.POST: rol_actual.eliminar_sprint= True
            else: rol_actual.eliminar_sprint= False
            if 'activar_sprint' in request.POST: rol_actual.activar_sprint= True
            else: rol_actual.activar_sprint= False
            if 'agregar_historia' in request.POST: rol_actual.agregar_historia= True
            else: rol_actual.agregar_historia= False
            if 'modificar_historia' in request.POST: rol_actual.modificar_historia= True
            else: rol_actual.modificar_historia= False
            if 'eliminar_historia' in request.POST: rol_actual.eliminar_historia= True
            else: rol_actual.eliminar_historia= False
            if 'adjuntar_archivos' in request.POST: rol_actual.adjuntar_archivos= True
            else: rol_actual.adjuntar_archivos= False
            if 'cargar_horas' in request.POST: rol_actual.cargar_horas= True
            else: rol_actual.cargar_horas= False
            if 'actualizar_estado' in request.POST: rol_actual.actualizar_estado= True
            else: rol_actual.actualizar_estado= False
            if 'ver_historial' in request.POST: rol_actual.ver_historial= True
            else: rol_actual.ver_historial= False
            if 'validar_historia' in request.POST: rol_actual.validar_historia= True
            else: rol_actual.validar_historia= False
            if 'crear_flujo' in request.POST: rol_actual.crear_flujo= True
            else: rol_actual.crear_flujo= False
            if 'modificar_flujo' in request.POST: rol_actual.modificar_flujo= True
            else: rol_actual.modificar_flujo= False
            if 'eliminar_flujo' in request.POST: rol_actual.eliminar_flujo= True
            else: rol_actual.eliminar_flujo= False
            if 'ver_tabla' in request.POST: rol_actual.ver_tabla= True
            else: rol_actual.ver_tabla= False
            rol_actual.save()
        return render(request, self.template_name, diccionario)

class EliminarRol(RolView):
    template_name = 'EliminarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        if rol_actual.nombre== 'Scrum Master':
            diccionario['error']= 'Rol: Scrum Master - No se puede eliminar'
            #diccionario[super(EliminarRol, self).context_object_name]= Rol.objects.filter(proyecto= proyecto_actual, activo= True)
            return render(request, super(EliminarRol, self).template_name, diccionario)
        roles= Rol.objects.filter(nombre= rol_actual.nombre, activo= True)
        for rol_actual in roles:
            rol_actual.activo= False
            rol_actual.save()
        return render(request, self.template_name, diccionario)

class ConsultarRol(RolView):
    template_name = 'ConsultarUsuarios.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['rol']= rol_actual
        diccionario['lista_roles']= Rol.objects.filter(nombre=rol_actual.nombre, activo= True)
        return render(request, self.template_name, diccionario)

class DesasignarRol(RolView):
    template_name = 'DesasignarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        if rol_actual.nombre== 'Scrum Master':
            diccionario['error']= 'Rol: Scrum Master - Operacion No Permitida'
            #diccionario[super(DesasignarRol, self).context_object_name]= Rol.objects.filter( activo= True)
            return render(request, super(DesasignarRol, self).template_name, diccionario)
        rol_actual.activo= False
        rol_actual.save()
        if len(Rol.objects.filter(nombre= rol_actual.nombre))==1:
            diccionario['error']= 'No existe usuarios asignados a dicho rol - Rol Eliminado'

        return render(request, self.template_name, diccionario)

class AsignarRol(RolView):
    template_name = 'AsignarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        diccionario['rol']= rol_actual
        if rol_actual.nombre== 'Scrum Master':
            diccionario['error']= 'Rol: Scrum Master - Operacion No Permitida'
            #diccionario[super(AsignarRol, self).context_object_name]= Rol.objects.filter( activo= True)
            return render(request, super(AsignarRol, self).template_name, diccionario)
        usuarios_rol= []    #Usuarios que pertenecen al Rol

        for i in Rol.objects.filter(nombre= rol_actual.nombre, activo= True):
            usuarios_rol.append(i.usuario)
        not_usuarios_rol= []     #Usuarios que no pertenecen al Rol
        for i in Usuario.objects.all():
            if not (i in usuarios_rol): not_usuarios_rol.append(i)
        if not len(not_usuarios_rol):
            diccionario['error']= 'Todos los usuarios tienen asignados este rol'
            diccionario[super(AsignarRol, self).context_object_name]= Rol.objects.filter( activo= True)
            return render(request, super(AsignarRol,self).template_name, diccionario)
        else:
            diccionario['lista_usuarios']= not_usuarios_rol
            return render(request, self.template_name, diccionario)

class AsignarRolConfirm(RolView):
    template_name = 'AsignarRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        rol_actual= Rol.objects.get(id= request.POST['rol'])
        usuario_rol= Usuario.objects.get(username= request.POST['usuario'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual
        diccionario['rol']= rol_actual

        nuevo_rol= Rol(
            nombre= rol_actual.nombre,
            usuario= usuario_rol,
            crear_proyecto= rol_actual.crear_proyecto,
            modificar_proyecto= rol_actual.modificar_proyecto,
            eliminar_proyecto= rol_actual.eliminar_proyecto,
            cerrar_proyecto= rol_actual.cerrar_proyecto,
            crear_usuario= rol_actual.crear_usuario,
            modificar_usuario= rol_actual.modificar_usuario,
            eliminar_usuario= rol_actual.eliminar_usuario,
            agregar_rol= rol_actual.agregar_rol,
            modificar_rol= rol_actual.modificar_rol,
            eliminar_rol= rol_actual.eliminar_rol,
            generar_resumen_clientes= rol_actual.generar_resumen_clientes,
            generar_burndown= rol_actual.generar_burndown,
            asignar_usuario_inicial= rol_actual.asignar_usuario_inicial,
            asignar_permisos_roles= rol_actual.asignar_permisos_roles,
            asignar_roles_usuario= rol_actual.asignar_roles_usuario,
            asignar_usuarios_proyecto= rol_actual.asignar_usuarios_proyecto,
            listar_usuarios= rol_actual.listar_usuarios,
            listar_proyectos= rol_actual.listar_proyectos,
            agregar_sprint= rol_actual.agregar_sprint,
            modificar_sprint= rol_actual.modificar_sprint,
            eliminar_sprint= rol_actual.eliminar_sprint,
            activar_sprint= rol_actual.activar_sprint,
            agregar_historia= rol_actual.agregar_historia,
            modificar_historia= rol_actual.modificar_historia,
            eliminar_historia= rol_actual.eliminar_historia,
            adjuntar_archivos= rol_actual.adjuntar_archivos,
            cargar_horas= rol_actual.cargar_horas,
            actualizar_estado= rol_actual.actualizar_estado,
            ver_historial= rol_actual.ver_historial,
            validar_historia= rol_actual.validar_historia,
            crear_flujo= rol_actual.crear_flujo,
            modificar_flujo= rol_actual.modificar_flujo,
            eliminar_flujo= rol_actual.eliminar_flujo,
            ver_tabla= rol_actual.ver_tabla,
        )

        nuevo_rol.save()
        return render(request, self.template_name, diccionario)