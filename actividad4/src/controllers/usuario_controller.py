from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from src.models.entities.usuario import Usuario
from src.models.services.computador_service import ComputadorService
from src.models.services.usuario_service import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/usuario")


@usuario_bp.route("/", methods=["GET"])
@usuario_bp.route("/listar_todo", methods=["GET"])
def listar_usuarios():
    usuario_service: UsuarioService = current_app.usuario_service
    computador_service: ComputadorService = current_app.computador_service

    usuarios = usuario_service.obtener_todos_los_usuarios()
    computadores = computador_service.obtener_todos_los_computadores()

    return render_template(
        "forms/usuarios/listar_todo.html",
        usuarios=usuarios,
        computadores=computadores,
    )


@usuario_bp.route("/agregar", methods=["GET"])
def mostrar_formulario_agregar():
    return render_template("forms/usuarios/agregar.html")


@usuario_bp.route("/guardar", methods=["POST"])
def guardar_usuario():
    usuario_service: UsuarioService = current_app.usuario_service

    username = request.form["username"]
    password = request.form["password"]
    nombre = request.form["nombre"]
    email = request.form["email"]

    nuevo_usuario = Usuario(
        username=username, password=password, nombre=nombre, email=email
    )
    usuario_service.crear_usuario(nuevo_usuario)

    flash("Usuario agregado exitosamente.", "success")
    return redirect(url_for("usuario_bp.listar_usuarios"))


@usuario_bp.route("/editar", methods=["GET"])
def mostrar_formulario_editar():
    usuario_service: UsuarioService = current_app.usuario_service

    usuario_id = request.args.get("id", type=int)
    usuario = usuario_service.obtener_usuario_por_id(usuario_id)

    if usuario:
        return render_template("forms/usuarios/editar.html", usuario=usuario)
    else:
        flash("Usuario no encontrado para editar.", "danger")
        return redirect(url_for("usuario_bp.listar_usuarios"))


@usuario_bp.route("/actualizar", methods=["POST"])
def actualizar_usuario():
    usuario_service: UsuarioService = current_app.usuario_service

    usuario_id = request.form.get("id", type=int)

    usuario_existente = usuario_service.obtener_usuario_por_id(usuario_id)

    if usuario_existente:
        usuario_existente.username = request.form["username"]
        usuario_existente.password = request.form["password"]
        usuario_existente.nombre = request.form["nombre"]
        usuario_existente.email = request.form["email"]

        usuario_service.actualizar_usuario(usuario_existente)
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("usuario_bp.listar_usuarios"))
    else:
        flash(
            f"Error: Usuario con ID {usuario_id} no encontrado para actualizar.",
            "danger",
        )
        return redirect(url_for("usuario_bp.listar_usuarios"))


@usuario_bp.route("/eliminar", methods=["GET"])
def eliminar_usuario():
    usuario_service: UsuarioService = current_app.usuario_service
    usuario_id = request.args.get("id", type=int)

    if not usuario_id:
        flash("ID de usuario no proporcionado para eliminar.", "danger")
        return redirect(url_for("usuario_bp.listar_usuarios"))

    usuario_service.eliminar_usuario(usuario_id)
    flash("Usuario eliminado.", "success")
    return redirect(url_for("usuario_bp.listar_usuarios"))


@usuario_bp.route("/buscar", methods=["GET"])
def mostrar_formulario_buscar():
    return render_template("forms/usuarios/buscar.html")


@usuario_bp.route("/buscar", methods=["POST"])
def buscar_usuario():
    usuario_service: UsuarioService = current_app.usuario_service
    criterio = request.form.get("criterio", "")

    usuario_encontrado = usuario_service.obtener_usuario_por_username(criterio)

    return render_template(
        "forms/usuarios/buscar_resultado.html",
        usuarioEncontrado=usuario_encontrado,
        criterio=criterio,
    )


@usuario_bp.route("/login", methods=["GET"])
def mostrar_formulario_login():
    return render_template("forms/usuarios/login.html")


@usuario_bp.route("/login", methods=["POST"])
def procesar_login():
    usuario_service: UsuarioService = current_app.usuario_service

    username_or_email = request.form["username"]
    password = request.form["password"]
    admin_login = request.form.get("adminLogin")

    if (
        admin_login == "true"
        and username_or_email == "admin"
        and password == "admin"
    ):
        session["usuarioLogueado_id"] = -1
        session["usuarioLogueado_username"] = "admin"
        flash("Bienvenido Administrador!", "info")
        return redirect(url_for("usuario_bp.listar_usuarios"))

    usuario = usuario_service.autenticar_usuario(username_or_email, password)
    if usuario:
        session["usuarioLogueado_id"] = usuario.id
        session["usuarioLogueado_username"] = usuario.username
        flash(f"Bienvenido, {usuario.username}!", "success")
        return redirect(url_for("usuario_bp.mostrar_detalles_usuario"))
    else:
        flash("Credenciales inválidas.", "danger")
        return render_template("forms/usuarios/login.html")


@usuario_bp.route("/listar", methods=["GET"])
def mostrar_detalles_usuario():
    usuario_service: UsuarioService = current_app.usuario_service

    usuario_id_logueado = session.get("usuarioLogueado_id")
    usuario_username_logueado = session.get("usuarioLogueado_username")

    if usuario_id_logueado is None:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for("usuario_bp.mostrar_formulario_login"))

    if usuario_id_logueado == -1 and usuario_username_logueado == "admin":
        usuario_logueado = Usuario(
            username="admin", password="", nombre="Administrador", email=""
        )
        usuario_logueado.id = -1
    else:
        usuario_logueado = usuario_service.obtener_usuario_por_id(
            usuario_id_logueado
        )

        if not usuario_logueado:
            session.pop("usuarioLogueado_id", None)
            session.pop("usuarioLogueado_username", None)
            flash("Tu sesión ha expirado o el usuario no existe.", "danger")
            return redirect(url_for("usuario_bp.mostrar_formulario_login"))

    print(
        f"DEBUG (Flask): usuarioLogueado en sesión: {usuario_logueado.username if usuario_logueado else 'None'}"
    )

    return render_template(
        "forms/usuarios/listar.html", usuarioLogueado=usuario_logueado
    )


@usuario_bp.route("/logout", methods=["GET"])
def cerrar_sesion():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("usuario_bp.mostrar_formulario_login"))


@usuario_bp.route("/recordar_password", methods=["GET"])
def mostrar_formulario_recordar_password():
    return render_template("forms/usuarios/recordar_password.html")


@usuario_bp.route("/recordar_password", methods=["POST"])
def procesar_recordar_password():
    usuario_service: UsuarioService = current_app.usuario_service

    identifier = request.form.get("identifier")

    usuario = usuario_service.iniciar_recordar_password(identifier)

    if usuario:
        usuario_service.send_password_recovery_email(usuario)
        flash(
            "Si el correo o nombre de usuario existe,"
            " se ha enviado un correo con la contraseña.",
            "info",
        )
    else:
        flash(
            "Si el correo o nombre de usuario existe,"
            " se ha enviado un correo con la contraseña.",
            "info",
        )

    return render_template("forms/usuarios/recordar_password.html")


@usuario_bp.route("/listar", methods=["GET"])
def listar_usuario():
    if "usuario_id" not in session:
        return redirect(url_for("usuario_bp.mostrar_formulario_login"))

    usuario_id = session["usuario_id"]
    usuario_service = current_app.usuario_service
    usuario = usuario_service.obtener_usuario_por_id(usuario_id)

    if usuario:
        return render_template(
            "forms/usuarios/listar.html", usuarioLogueado=usuario
        )
    else:
        session.pop("usuario_id", None)
        session.pop("username", None)
        return redirect(url_for("usuario_bp.mostrar_formulario_login"))
