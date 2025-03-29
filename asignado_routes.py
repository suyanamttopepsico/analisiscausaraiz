from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from flask_login import current_user, login_required
import os
from manejoBasesSQL import *
from manejoSAP2 import *
from procesamiento import *

UPLOAD_FOLDER = 'static/uploads/'
asignado_routes = Blueprint('asignado', __name__)

def initialize_data():
    if 'asignado' not in session:
        session['asignado'] = {'Actualizado': False}

@asignado_routes.route("/", methods=["GET", "POST"])
@login_required
def asignado():
    initialize_data()
    # En este endpoint se podría actualizar únicamente la sesión sin ejecutar la función,
    # pero en nuestro caso se centraliza la actualización en /run_function
    return render_template("bibliotecaAsignados.html", 
                           titulo=("Actualizado" if session['asignado'].get('Actualizado') else "No actualizado"),
                           datos=session['asignado'])

@asignado_routes.route('/run_function', methods=['POST'])
@login_required
def run_function():
    initialize_data()
    
    # Asigna el código de planta según el valor del usuario
    planta_actual = current_user.plant
    if planta_actual == "Suyana":
         codplanta = 8600
    elif planta_actual == "Funza":
         codplanta = 8700
    else:
         codplanta = None  # O definir un valor por defecto

    # Actualiza las fechas en la sesión usando los datos enviados desde el formulario
    asignado_data = session.get('asignado', {})
    asignado_data['Fecha_Inicio'] = request.form.get('fechaInicio', asignado_data.get('Fecha_Inicio'))
    asignado_data['Fecha_Fin'] = request.form.get('fechaFin', asignado_data.get('Fecha_Fin'))

    try:
         # Se asume que esta función procesa la información de SAP
         lecturaSAPandinos(asignado_data['Fecha_Inicio'], asignado_data['Fecha_Fin'], codplanta)
         df_38=txtIW38(asignado_data['Fecha_Inicio'], asignado_data['Fecha_Fin'])
         asignado_data['Actualizado'] = True
    except Exception as e:
         print(f"Error al ejecutar lecturaSAPandinos: {e}")
         asignado_data['Actualizado'] = False

    session['asignado'] = asignado_data

    titulo = "Actualizado" if asignado_data.get('Actualizado') else "No actualizado"
    return render_template("bibliotecaAsignados.html", titulo=titulo, datos=asignado_data)
