from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from src.models.entities.computador import Computador
# from src.models.entities.usuario import Usuario
from src.models.services.computador_service import ComputadorService
from src.models.services.usuario_service import UsuarioService

computador_bp = Blueprint("computador_bp", __name__, url_prefix="/computadores")


@computador_bp.route("/", methods=["GET"])
@computador_bp.route("/listar_todo", methods=["GET"])
def listar_computadores():
    computador_service: ComputadorService = current_app.computador_service
    computadores = computador_service.obtener_todos_los_computadores()
    return render_template(
        "forms/computadores/listar_todo.html", computadores=computadores
    )


@computador_bp.route("/agregar", methods=["GET"])
def mostrar_formulario_agregar():
    computador = Computador(
        marca="",
        categoria="",
        marca_cpu="",
        velocidad_cpu=0.0,
        tecnologia_ram="",
        capacidad_ram=0,
        tecnologia_disco="",
        capacidad_disco=0,
        num_puertos_usb=0,
        num_puertos_hdmi=0,
        marca_monitor="",
        pulgadas=0.0,
        precio=0.0,
    )

    usuario_service: UsuarioService = current_app.usuario_service
    usuarios = usuario_service.obtener_todos_los_usuarios()

    return render_template(
        "forms/computadores/agregar.html",
        computador=computador,
        usuarios=usuarios,
    )


@computador_bp.route("/guardar", methods=["POST"])
def guardar_computador():
    computador_service: ComputadorService = current_app.computador_service
    usuario_service: UsuarioService = current_app.usuario_service

    usuario_id = request.form.get("usuario_id", type=int)
    usuario_obj = None
    if usuario_id:
        usuario_obj = usuario_service.obtener_usuario_por_id(usuario_id)

    nuevo_computador = Computador(
        marca=request.form["marca"],
        categoria=request.form["categoria"],
        marca_cpu=request.form["marca_cpu"],
        velocidad_cpu=float(request.form["velocidad_cpu"]),
        tecnologia_ram=request.form["tecnologia_ram"],
        capacidad_ram=int(request.form["capacidad_ram"]),
        tecnologia_disco=request.form["tecnologia_disco"],
        capacidad_disco=int(request.form["capacidad_disco"]),
        num_puertos_usb=int(request.form["num_puertos_usb"]),
        num_puertos_hdmi=int(request.form["num_puertos_hdmi"]),
        marca_monitor=request.form["marca_monitor"],
        pulgadas=float(request.form["pulgadas"]),
        precio=float(request.form["precio"]),
        usuario=usuario_obj,
    )
    computador_service.crear_computador(nuevo_computador)
    flash("Computador agregado exitosamente.", "success")
    return redirect(url_for("usuario_bp.listar_usuarios"))


@computador_bp.route("/editar", methods=["GET"])
def mostrar_formulario_editar():
    computador_service: ComputadorService = current_app.computador_service
    usuario_service: UsuarioService = current_app.usuario_service

    computador_id = request.args.get("id", type=int)
    computador = computador_service.obtener_computador_por_id(computador_id)

    if not computador:
        flash("Computador no encontrado.", "danger")
        return redirect(url_for("computador_bp.listar_computadores"))

    usuarios = usuario_service.obtener_todos_los_usuarios()

    return render_template(
        "forms/computadores/editar.html",
        computador=computador,
        usuarios=usuarios,
    )


@computador_bp.route("/actualizar", methods=["POST"])
def actualizar_computador():
    computador_service: ComputadorService = current_app.computador_service
    usuario_service: UsuarioService = current_app.usuario_service

    computador_id = request.form.get("id", type=int)
    computador_existente = computador_service.obtener_computador_por_id(
        computador_id
    )

    if not computador_existente:
        flash("Error: Computador a actualizar no encontrado.", "danger")
        return redirect(url_for("computador_bp.listar_computadores"))

    computador_existente.marca = request.form["marca"]
    computador_existente.categoria = request.form["categoria"]
    computador_existente.marca_cpu = request.form["marca_cpu"]
    computador_existente.velocidad_cpu = float(request.form["velocidad_cpu"])
    computador_existente.tecnologia_ram = request.form["tecnologia_ram"]
    computador_existente.capacidad_ram = int(request.form["capacidad_ram"])
    computador_existente.tecnologia_disco = request.form["tecnologia_disco"]
    computador_existente.capacidad_disco = int(request.form["capacidad_disco"])
    computador_existente.num_puertos_usb = int(request.form["num_puertos_usb"])
    computador_existente.num_puertos_hdmi = int(
        request.form["num_puertos_hdmi"]
    )
    computador_existente.marca_monitor = request.form["marca_monitor"]
    computador_existente.pulgadas = float(request.form["pulgadas"])
    computador_existente.precio = float(request.form["precio"])

    usuario_id = request.form.get("usuario_id", type=int)
    if usuario_id:
        usuario_obj = usuario_service.obtener_usuario_por_id(usuario_id)
        if usuario_obj:
            computador_existente.usuario = usuario_obj
        else:
            flash(
                f"Advertencia: Usuario con ID {usuario_id} no encontrado. "
                "Relación no establecida.",
                "warning",
            )
    else:
        computador_existente.usuario = None

    computador_service.actualizar_computador(computador_existente)
    flash("Computador actualizado correctamente.", "success")
    return redirect(url_for("usuario_bp.listar_usuarios"))


@computador_bp.route("/eliminar", methods=["GET"])
def eliminar_computador():
    computador_service: ComputadorService = current_app.computador_service
    computador_id = request.args.get("id", type=int)

    if not computador_id:
        flash("ID de computador no proporcionado para eliminar.", "danger")
        return redirect(url_for("computador_bp.listar_computadores"))

    computador_service.eliminar_computador(computador_id)
    flash("Computador eliminado.", "success")
    return redirect(url_for("usuario_bp.listar_usuarios"))


@computador_bp.route("/buscar", methods=["GET"])
def mostrar_formulario_buscar():
    return render_template("forms/computadores/buscar.html")


@computador_bp.route("/buscar", methods=["POST"])
def buscar_computador():
    computador_service: ComputadorService = current_app.computador_service
    criterio = request.form.get("criterio", "")

    resultados = computador_service.buscar_computadores_por_criterio(criterio)
    return render_template(
        "forms/computadores/buscar_resultado.html",
        computadoresEncontrados=resultados,
        criterio=criterio,
    )

