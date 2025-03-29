from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename

TEMP_UPLOAD_FOLDER = 'static/uploads/temp/'
UPLOAD_FOLDER = 'static/uploads/'
problema_routes = Blueprint('problema', __name__)

def get_user_temp_folder(username):
    """Crea una carpeta temporal para el usuario si no existe."""
    user_folder = os.path.join(TEMP_UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

# Inicializar datos en la sesión
def initialize_data():
    if 'problema' not in session:
        session['problema'] = {}
    if 'evento' not in session:
        session['evento'] = {}
    if 'imagen_averia' not in session:
        session['imagen_averia']=[]
        
@problema_routes.route("/", methods=["GET", "POST"])
@login_required
def problema():
    
    initialize_data()
    username = current_user.username
    user_temp_folder = get_user_temp_folder(username)
    #print(session['imagen_averia'])
    # Si hay datos en la sesión, usar las rutas de imágenes previamente guardadas
    imagenes_session=session['imagen_averia']
    
    if request.method == "POST":
        componente = request.form['componente']
        parteComponente = request.form['parteComponente']
        difiereEstadoNormal = request.form['difiereEstadoNormal']
        repetitivo = request.form['repetitivo']
        previo = request.form['previo']
        detallesRepetitivo = request.form['detallesRepetitivo']
        detallesPrevio = request.form['detallesPrevio']
        
        # Manejar múltiples imágenes
    
        imagenesAveria = request.files.getlist('imagenAveria')
        for imagenAveria in imagenesAveria:
            if imagenAveria and imagenAveria.filename != "":
                filename = secure_filename(imagenAveria.filename)
                file_extension = os.path.splitext(filename)[1]
                unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{file_extension}"
                imagen_path = os.path.join(user_temp_folder, unique_filename)
                imagenAveria.save(imagen_path)
                imagenes_pathname=f"/{imagen_path}"
                               
                imagenes_session.append({
                    "Indice": len(imagenes_session)+1,
                    'Imagen_de_Averia':imagenes_pathname
                })
                session['imagen_averia']=imagenes_session
    


        # Guardar los datos en la sesión, incluyendo las rutas de las imágenes
        session['problema'] = {
            'Componente': componente,
            'Parte_de_Componente': parteComponente,
            'Difiere_estado_normal': difiereEstadoNormal,
            'Problema_repetitivo': repetitivo,
            'Problema_previo': previo,
            'Detalles_Problema_repetitivo': detallesRepetitivo,
            'Detalles_Problema_Previo': detallesPrevio,
            'Autor': current_user.username
        }
        #print('Imagenes de la sesion que se van a guardar')
        #print(session['imagen_averia'])
        evento_data = session.get('evento', {})
        evento_data['Titulo'] = f"{componente.capitalize()} :{parteComponente.capitalize()}, {difiereEstadoNormal.lower()}"
        session['evento'] = evento_data

        # Redirigir dependiendo de la acción
        if request.form['action'] == 'equipo':
            return redirect(url_for('equipo.equipo'))
        elif request.form['action'] == 'evento':
            return redirect(url_for('evento.evento'))
        elif request.form['action']=='bases':
            return redirect(url_for('bases.bases'))
    
    return render_template("problema.html", datos=session['problema'],imagenes=session['imagen_averia'])

@problema_routes.route("/delete_image", methods=["POST"])
@login_required
def delete_image():
    initialize_data()  # Asegúrate de que la sesión esté inicializada

    data = request.get_json()
    index = data.get('index')  # Índice de la imagen a eliminar

    if index is not None:
        imagenes_session = session['imagen_averia']
        
        # Buscar y eliminar la imagen correspondiente
        imagen_eliminada = None
        for imagen in imagenes_session:
            if imagen['Indice'] == index:
                imagen_eliminada = imagen
                break

        if imagen_eliminada:
            # Eliminar la imagen de la sesión
            imagenes_session.remove(imagen_eliminada)
            session['imagen_averia'] = imagenes_session

            # Eliminar el archivo físico si es necesario
            imagen_path = os.path.join(os.getcwd(), imagen_eliminada['Imagen_de_Averia'][1:])  # Quita el "/" inicial
            if os.path.exists(imagen_path):
                os.remove(imagen_path)

            # Eliminar de la base de datos (si corresponde)
            # Aquí puedes agregar tu lógica para interactuar con la base de datos SQL
            # Por ejemplo: eliminar la entrada asociada a la imagen eliminada
            # db.execute("DELETE FROM tabla_imagenes WHERE id = %s", (imagen_id,))

            return render_template("problema.html", datos=session['problema'],imagenes=session['imagen_averia'])
    
    return render_template("problema.html", datos=session['problema'],imagenes=session['imagen_averia'])

