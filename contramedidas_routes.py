from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
contramedidas_routes = Blueprint('contramedidas', __name__)

# Inicializar datos en la sesión
def initialize_data():
    
    if 'contramedidas' not in session:
        session['contramedidas'] = []

@contramedidas_routes.route("/", methods=["GET", "POST"])
def contramedidas():

    initialize_data()
    contramedidas=session['contramedidas']
    if request.method == "POST":

        contramedidas.append({
            "Indice": len(contramedidas)+1,
            "Tipo": request.form.get('tipo'),
            'Descripcion_breve': request.form.get('descripcionBreve'),
            'OT_SAP': request.form.get('otSAP'),
            'Fecha_de_cumplimiento': request.form.get('fechaCumplimiento'),
            'OT_Completado': request.form.get('completado'),
            'Autor':current_user.username 
        })
        session['contramedidas']=contramedidas
        
    return render_template("contramedidas.html", contramedidas=session['contramedidas'])

# Ruta para eliminar una fila según el índice y resetear los índices restantes
@contramedidas_routes.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    initialize_data()
    contramedidas = session['contramedidas']

    # Filtrar la lista para eliminar la fila con el índice especificado
    contramedidas = [row for row in contramedidas if row["Indice"] != index]

    # Resetear el índice de cada fila para que sean secuenciales
    for i, row in enumerate(contramedidas, start=1):
        row["Indice"] = i

    session['contramedidas'] = contramedidas

    return redirect(url_for("contramedidas.contramedidas"))

# Ruta para editar una fila
@contramedidas_routes.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    initialize_data()
    contramedidas = session['contramedidas']

    # Buscar la fila que se va a editar
    row_to_edit = next((row for row in contramedidas if row["Indice"] == index), None)

    if request.method == "POST":

        # Actualizar la descripción
      
        row_to_edit['Tipo']= request.form.get('tipo')
        row_to_edit['Descripcion_breve']= request.form.get('descripcionBreve')
        row_to_edit['OT_SAP']= request.form.get('otSAP')
        row_to_edit['Fecha_de_cumplimiento']= request.form.get('fechaCumplimiento')
        row_to_edit['OT_Completado'] = request.form.get('completado')

        # Guardar los cambios en la sesión
        session['contramedidas'] = contramedidas
        return redirect(url_for("contramedidas.contramedidas"))

    return render_template("editContramedidas.html", row=row_to_edit, completado=row_to_edit['OT_Completado'],contramedidas=session['contramedidas'])

