from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename

from manejoBases import *

UPLOAD_FOLDER = 'static/uploads/'
TEMP_UPLOAD_FOLDER = 'static/uploads/temp/'
condiciones_routes = Blueprint('condiciones', __name__)

# Inicializar datos en la sesión
def initialize_data():
    if 'equipo' not in session:
        session['equipo'] = {}
    if 'secuencias' not in session:
        session['secuencias'] = []
    if 'condiciones' not in session:
        session['condiciones'] = []

def get_user_temp_folder(username):
    """Crea una carpeta temporal para el usuario si no existe."""
    user_folder = os.path.join(TEMP_UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

@condiciones_routes.route("/", methods=["GET", "POST"])
def condiciones():
    username = current_user.username
    user_temp_folder = get_user_temp_folder(username)
    initialize_data()
    data = session.get('condiciones', {})
    secuencia = session['secuencia_id']
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        imagen = request.files["imagen"]
        
        imagenes_pathname=""
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{file_extension}"
            imagen_path = os.path.join(user_temp_folder, unique_filename)
            imagen.save(imagen_path)
            imagenes_pathname=f"/{imagen_path}"
        
        filtro = [item for item in data if item["Secuencia"] == secuencia]

        new_indice = len(data) + 1  # Determinar el índice secuencial
        new_orden = len(filtro) + 1
        data.append({
            "Indice": new_indice,
            "Descripcion": descripcion,
            "Imagen": imagenes_pathname,  # Puede ser una ruta o vacío si no se cargó imagen
            "Secuencia": secuencia,
            'Autor':current_user.username,
            'Orden':new_orden
        })
        session['condiciones'] = data  
    # Actualizar la sesión con la lista de registros

    # Convertir la lista de registros a un DataFrame para facilitar su manejo
    df = pd.DataFrame(session['condiciones'])
    if df.empty or df.shape[1] == 0:
        filtro = df
    else:
        filtro = df[df["Secuencia"] == secuencia]
        
    return render_template("condiciones.html", data=filtro.to_dict('records'))

# Ruta para eliminar una fila según el índice y resetear los índices restantes
@condiciones_routes.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    initialize_data()
    data = session['condiciones']

    # Filtrar la lista para eliminar la fila con el índice especificado
    data = [row for row in data if row["Indice"] != index]

    # Resetear el índice de cada fila para que sean secuenciales
    for i, row in enumerate(data, start=1):
        row["Indice"] = i

    session['condiciones'] = data  # Actualizar la sesión con la lista modificada

    return redirect(url_for("condiciones.condiciones"))

# Ruta para editar una fila
@condiciones_routes.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    username = current_user.username
    user_temp_folder = get_user_temp_folder(username)
    initialize_data()
    data = session['condiciones']
    #print(f"Antes de la edición: {data}")
    secuencia = session['secuencia_id']
    # Buscar la fila que se va a editar
    row_to_edit = next((row for row in data if row["Indice"] == index), None)

    if request.method == "POST":
        descripcion = request.form["descripcion"]
        imagen = request.files["imagen"]

        # Actualizar la descripción
        row_to_edit["Descripcion"] = descripcion

        # Si se sube una nueva imagen, actualizar el path
        if imagen:
            filename = secure_filename(imagen.filename)
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{file_extension}"
            imagen_path = os.path.join(user_temp_folder, unique_filename)
            imagen.save(imagen_path)
            imagen_pathname=f"{imagen_path}"
            row_to_edit["Imagen"] = f"/{imagen_pathname}"  # Actualizar la ruta de la imagen

        # Guardar los cambios en la sesión
        session['condiciones'] = data
        return redirect(url_for("condiciones.condiciones"))
        # Convertir la lista de registros a un DataFrame para facilitar su manejo
    df = pd.DataFrame(session['condiciones'])
    if df.empty or df.shape[1] == 0:
        filtro = df
    else:
        filtro = df[df["Secuencia"] == secuencia]
    
    #print(f"Fila editada: {row_to_edit}")
    #print(f"Después de la edición: {data}")


    return render_template("edit.html", row=row_to_edit, data=filtro.to_dict('records'))

# Ruta para mover una fila hacia arriba
@condiciones_routes.route("/move_up/<int:index>", methods=["POST"])
def move_up(index):
    initialize_data()
    data = session['condiciones']

    # Encontrar el índice de la fila actual
    idx = next((i for i, row in enumerate(data) if row["Indice"] == index), None)

    # Si no es la primera fila, mover hacia arriba
    if idx > 0:
        data[idx], data[idx - 1] = data[idx - 1], data[idx]  # Intercambiar las filas

    # Resetear los índices
    for i, row in enumerate(data, start=1):
        row["Indice"] = i

    session['condiciones'] = data  # Actualizar la sesión
    return redirect(url_for("condiciones.condiciones"))

# Ruta para mover una fila hacia abajo
@condiciones_routes.route("/move_down/<int:index>", methods=["POST"])
def move_down(index):
    initialize_data()
    data = session['condiciones']

    # Encontrar el índice de la fila actual
    idx = next((i for i, row in enumerate(data) if row["Indice"] == index), None)

    # Si no es la última fila, mover hacia abajo
    if idx is not None and idx < len(data) - 1:
        data[idx], data[idx + 1] = data[idx + 1], data[idx]  # Intercambiar las filas

    # Resetear los índices
    for i, row in enumerate(data, start=1):
        row["Indice"] = i

    session['condiciones'] = data  # Actualizar la sesión
    return redirect(url_for("condiciones.condiciones"))
