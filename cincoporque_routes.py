from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
cincoporque_routes = Blueprint('cincoporque', __name__)

# Inicializar datos en la sesión
def initialize_data():
    if 'cincoporque' not in session:
        session['cincoporque'] = {}

# Ruta principal para ingresar el equipo
@cincoporque_routes.route("/", methods=["GET", "POST"])
@login_required
def cincoporque():
    
    initialize_data()
    if request.method == "POST":

        primerPorque= request.form['primerPorque']
        segundoPorque= request.form['segundoPorque']
        tercerPorque= request.form['tercerPorque']
        cuartoPorque= request.form['cuartoPorque']
        quintoPorque= request.form['quintoPorque']
        primeraRespuesta= request.form['primeraRespuesta']
        segundaRespuesta= request.form['segundaRespuesta']
        terceraRespuesta= request.form['terceraRespuesta']
        cuartaRespuesta= request.form['cuartaRespuesta']
        quintaRespuesta= request.form['quintaRespuesta']
        tipoDeAveria= request.form['tipoDeAveria']

        session['cincoporque'] = {
            'Primer_porque': primerPorque,
            'Segundo_porque': segundoPorque,
            'Tercer_porque': tercerPorque,
            'Cuarto_porque': cuartoPorque,
            'Quinto_porque': quintoPorque,
            'Primera_respuesta': primeraRespuesta,
            'Segunda_respuesta': segundaRespuesta,
            'Tercera_respuesta': terceraRespuesta,
            'Cuarta_respuesta': cuartaRespuesta,
            'Quinta_respuesta': quintaRespuesta,
            'Tipo_de_averia': tipoDeAveria,
            'Autor':current_user.username 
        }
        if request.form['action'] == 'fenomeno':
            return redirect(url_for('fenomeno.fenomeno'))
        elif request.form['action'] == 'contramedidas':
            return redirect(url_for('contramedidas.contramedidas'))
        elif request.form['action']=='bases':
            return redirect(url_for('bases.bases'))
    return render_template("cincoporque.html", cincoporque=session['cincoporque'])

