from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename
from flask import request, jsonify

from manejoBases import *

UPLOAD_FOLDER = 'static/uploads/'
TEMP_UPLOAD_FOLDER = 'static/uploads/temp/'
equipo_routes = Blueprint('equipo', __name__)

def get_user_temp_folder(username):
    """Crea una carpeta temporal para el usuario si no existe."""
    user_folder = os.path.join(TEMP_UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder


# Inicializar datos en la sesión
def initialize_data():
    if 'equipo' not in session:
        session['equipo'] = {}
    if 'secuencia' not in session:
        session['secuencia'] = []
    if 'condiciones' not in session:
        session['condiciones'] = []

# Ruta principal para ingresar el equipo
@equipo_routes.route("/", methods=["GET", "POST"])
def equipo():
    username = current_user.username
    user_temp_folder = get_user_temp_folder(username)
    initialize_data()

    # Si hay datos previos en la sesión, usar la ruta de la imagen guardada (si existe)
    imagen_path = session['equipo'].get('Imagen', '')  # Usar imagen de la sesión si existe

    if request.method == "POST":
        nombre_equipo = request.form["nombre_equipo"]
        imagen = request.files["imagen_equipo"]
        fabricante = request.form["fabricante_equipo"]
        detalles = request.form["detalles_tecnicos"]
        imagenes_pathname=imagen_path
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{file_extension}"
            imagen_path = os.path.join(user_temp_folder, unique_filename)
            imagen.save(imagen_path)
            imagenes_pathname=f"/{imagen_path}"

                            
        # Verificar si se subió una nueva imagen
        # if imagen and imagen.filename != "":
        #     filename = secure_filename(imagen.filename)
        #     imagen_path = os.path.join(UPLOAD_FOLDER, filename)
        #     imagen.save(imagen_path)
        #     imagen_path = f"/{imagen_path}"  # Ruta accesible para el frontend

        # Guardar los datos del equipo en la sesión, incluyendo la imagen (si se subió una nueva)
        session['equipo'] = {
            "Nombre": nombre_equipo,
            "Imagen": imagenes_pathname,
            "Fabricante": fabricante,
            "Detalles_Tecnicos": detalles,
            'Autor': current_user.username
        }

        print(session['equipo'])

        # Redirigir dependiendo de la acción
        if request.form['action'] == 'problema':
            return redirect(url_for('problema.problema'))
        elif request.form['action'] == 'fenomeno':
            return redirect(url_for('fenomeno.fenomeno'))
        elif request.form['action']=='bases':
            return redirect(url_for('bases.bases'))

    return render_template("equipo.html", equipo=session['equipo'], secuencias=session['secuencia'])


# Ruta para agregar secuencias al equipo
@equipo_routes.route("/add_secuencia", methods=["POST"])
def add_secuencia():
    initialize_data()
    secuencias = session['secuencia']

    secuencia_id = len(secuencias) + 1
    secuencia_nombre = request.form["secuencia_nombre"]

    secuencias.append({
        "Indice": secuencia_id,
        "Nombre": secuencia_nombre,
        'Autor':current_user.username 
    })

    session['secuencia'] = secuencias
    return redirect(url_for("equipo.equipo"))

# Ruta para eliminar secuencias
@equipo_routes.route("/delete_secuencia/<int:index>", methods=["POST"])
def delete_secuencia(index):
    initialize_data()
    secuencias = session['secuencia']
    secuencias = [seq for seq in secuencias if seq["Indice"] != index]

    # Resetear índices de secuencias
    for i, secuencia in enumerate(secuencias, start=1):
        secuencia["Indice"] = i

    session['secuencia'] = secuencias
    return redirect(url_for("equipo.equipo"))


@equipo_routes.route("/edit_secuencia/<int:index>", methods=["GET", "POST"])
def edit_secuencia(index):
    initialize_data()
    secuencias = session['secuencia']
    
    # Manejo del formulario POST
    if request.method == "POST":
        nueva_descripcion = request.form.get("secuencia_nombre")
        for secuencia in secuencias:
            if secuencia["Indice"] == index:
                secuencia["Nombre"] = nueva_descripcion
                break
        session['secuencia'] = secuencias
        return redirect(url_for("equipo.equipo"))
    
    # Renderizar formulario de edición (para GET)
    secuencia_a_editar = next((seq for seq in secuencias if seq["Indice"] == index), None)
    return render_template("editSecuencias.html", equipo=session['equipo'], secuencia=secuencia_a_editar, secuencias=session['secuencia'])

# Ruta para redirigir a condiciones con el número de secuencia
@equipo_routes.route("/secuencias/<int:secuencia_id>")
def secuencias(secuencia_id):
    initialize_data()
    session['secuencia_id'] = secuencia_id
    return redirect(url_for("condiciones.condiciones"))


@equipo_routes.route('/reset_imagen_equipo', methods=['POST'])
def reset_imagen_equipo():
    data = request.json
    datosequipo=session['equipo']
    datosequipo['Imagen']=""
    session['equipo']=datosequipo
    return jsonify({"success": True})

