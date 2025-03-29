from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
fenomeno_routes = Blueprint('fenomeno', __name__)

# Inicializar datos en la sesión
def initialize_data():
    if 'fenomeno' not in session:
        session['fenomeno'] = {}

# Ruta principal para ingresar el equipo
@fenomeno_routes.route("/", methods=["GET", "POST"])
@login_required
def fenomeno():
    
    initialize_data()
    if request.method == "POST":

        que= request.form['Que']
        cuando= request.form['Cuando']
        donde= request.form['Donde']
        como= request.form['Como']
        cual= request.form['Cual']
        quien= request.form['Quien']
        detallesHechos= request.form['detallesHechos']
        OPLfile= request.files['OPLfile']

                # Inicializar imagen_path como vacío por si no se carga ninguna imagen
        OPL_path = ""
        
        # Verificar si el usuario subió una imagen
        if OPLfile and OPLfile.filename != "":
                        # Generar un nombre único para la imagen usando la fecha y un UUID
            filename = secure_filename(OPLfile.filename)
            file_extension = os.path.splitext(filename)[1]  # Obtener la extensión del archivo
            
            # Crear un nombre único con fecha y UUID
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{file_extension}"
            
            # Crear el path de la imagen y guardarla
            OPL_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            OPLfile.save(OPL_path)
            OPL_path = f"/{OPL_path}"  # Ruta para HTML


        session['fenomeno'] = {
            'Que': que,
            'Cuando': cuando,
            'Donde': donde,
            'Como': como,
            'Cual': cual,
            'Quien': quien,
            'Detalles_de_los_hechos': detallesHechos,
            'OPL': OPL_path,
            'Autor':current_user.username 
        }
        if request.form['action'] == 'equipo':
            return redirect(url_for('equipo.equipo'))
        elif request.form['action'] == 'cincoporque':
            return redirect(url_for('cincoporque.cincoporque'))
        elif request.form['action']=='bases':
            return redirect(url_for('bases.bases'))
        
    return render_template("fenomeno.html", fenomeno=session['fenomeno'])

