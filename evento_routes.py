from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
evento_routes = Blueprint('evento', __name__)

# Inicializar datos en la sesión
def initialize_data():
    if 'evento' not in session:
        session['evento'] = {}
    # elif 'equipo' not in session:
    #     session['equipo'] = {}
    # elif 'secuencias' not in session:
    #     session['secuencias'] = []
    # elif 'data' not in session:
    #     session['data'] = []
    # elif 'problema' not in session:
    #     session['problema'] = {}
    # elif 'cincoporque' not in session:
    #     session['cincoporque'] = {}
    # elif 'contramedidas' not in session:
    #     session['contramedidas'] = []
    # elif 'fenomeno' not in session:
    #     session['fenomeno'] = {}

# Ruta principal para ingresar el equipo
@evento_routes.route("/", methods=["GET", "POST"])
@login_required
def evento():
    #print(f"Usuario autenticado: {current_user.is_authenticated}")
    #print(f"Usuario actual: {current_user.username if current_user.is_authenticated else 'Anónimo'}")
    initialize_data()
    if request.method == "POST":
        # Si 'evento' ya existe en la sesión, obtén su valor actual, si no, crea un diccionario vacío
        evento_data = session.get('evento', {})

        # Actualiza solo los valores que se han enviado en el formulario
        evento_data['Categoria'] = request.form.get('categoria', evento_data.get('Categoria'))
        evento_data['Fecha_Evento'] = request.form.get('fechaEvento', evento_data.get('Fecha_Evento'))
        evento_data['OT_Averia'] = request.form.get('otAveria', evento_data.get('OT_Averia'))
        evento_data['OT_RCA'] = request.form.get('otRca', evento_data.get('OT_RCA'))
        evento_data['Planta'] = request.form.get('planta', evento_data.get('Planta'))
        evento_data['Linea_Produccion'] = request.form.get('lineaProduccion', evento_data.get('Linea_Produccion'))
        evento_data['Area_Empresa'] = request.form.get('areaEmpresa', evento_data.get('Area_Empresa'))
        evento_data['Cod_SAP'] = request.form.get('codigoSap', evento_data.get('Cod_SAP'))
        evento_data['Nombre_Equipo_SAP'] = request.form.get('nombreEquipo', evento_data.get('Nombre_Equipo_SAP'))
        evento_data['Causa_RCA'] = request.form.get('causaRca', evento_data.get('Causa_RCA'))
        evento_data['Costos'] = request.form.get('costos', evento_data.get('Costos'))
        evento_data['Tiempo_Total'] = request.form.get('tiempoTotal', evento_data.get('Tiempo_Total'))
        evento_data['MTBF'] = request.form.get('MTBF', evento_data.get('MTBF'))
        evento_data['MTTR'] = request.form.get('MTTR', evento_data.get('MTTR'))
        evento_data['Tecnico'] = request.form.get('tecnicoEvento', evento_data.get('Tecnico'))
        evento_data['Representante_Mantenimiento'] = request.form.get('representanteMantenimiento', evento_data.get('Representante_Mantenimiento'))
        evento_data['Representante_SASS'] = request.form.get('representanteSass', evento_data.get('Representante_SASS'))
        evento_data['Representante_Calidad'] = request.form.get('representanteCalidad', evento_data.get('Representante_Calidad'))
        evento_data['Representante_Produccion'] = request.form.get('representanteProduccion', evento_data.get('Representante_Produccion'))
        evento_data['Terminado'] = evento_data.get('Terminado', False)
        evento_data['Aprobado'] = evento_data.get('Aprobado', False)
        evento_data['Aprobado_Regional'] = evento_data.get('Aprobado_Regional', False)
        evento_data['Aproador_Local'] = evento_data.get('Aproador_Local', "")
        evento_data['Calificacion'] = evento_data.get('Calificacion', 0)
        evento_data['Aprobador_Regional'] = evento_data.get('Aprobador_Regional', "")
        if 'Autor' not in evento_data or not evento_data['Autor']:
            evento_data['Autor'] = current_user.username
        


        # Guardar la actualización parcial en la sesión
        session['evento'] = evento_data

        if request.form['action'] == 'problema':
            return redirect(url_for('problema.problema'))
        elif request.form['action']=='bases':
            return redirect(url_for('bases.bases'))

    return render_template("evento.html", datos=session['evento'])

