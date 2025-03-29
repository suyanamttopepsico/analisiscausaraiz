from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
import pandas as pd
import os
from werkzeug.utils import secure_filename
from flask_login import current_user,login_required

from manejoBasesSQL import *


bases_routes = Blueprint('bases', __name__)




# Ruta principal para ingresar el equipo
@bases_routes.route("/", methods=["GET", "POST"])
def bases():
    if 'evento' in session:
        print('Proceso de guardar el evento')
        eventoID=agregarFilaID(session['evento'],"evento")
    if 'equipo' in session:
        print('Proceso de guardar el equipo')
        move_image_to_final('equipo',eventoID,current_user.username,columnasession='Imagen')
        print(session['equipo'])
        agregarFila([session['equipo']],"equipo","Evento",eventoID)  
        print('Proceso de guardar el equipo terminado')
    if 'secuencia' in session:
        print('Proceso de guardar secuencia')
        agregarFila(session['secuencia'],"secuencia","Evento",eventoID,'Indice')
        print('Proceso de guardar secuencia terminado')
    if 'condiciones' in session:
        print('Proceso de guardar condiciones')
        move_image_to_final_condiciones('condiciones',eventoID,current_user.username,columnasession='Imagen')
        print(session['condiciones'])
        agregarFila(session['condiciones'],"condiciones","Evento",eventoID,"Indice")
        print('Proceso de guardar condiciones terminado')
    if 'problema' in session:
        ID=agregarFila([session['problema']],"problema","Evento",eventoID)
        move_images_to_final('imagen_averia',eventoID, current_user.username)
        agregarFila(session['imagen_averia'],"imagen_averia","Evento",eventoID,'Indice')
    if 'cincoporque' in session:
        agregarFila([session['cincoporque']],"cincoporque","Evento",eventoID)
    if 'contramedidas' in session:
        agregarFila(session['contramedidas'],"contramedidas","Evento",eventoID,"Indice")
    if 'fenomeno' in session:
        agregarFila([session['fenomeno']],"fenomeno","Evento",eventoID)


    return redirect(url_for("login.welcome"))
