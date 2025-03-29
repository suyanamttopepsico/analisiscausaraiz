from flask import Flask, render_template, request, session, redirect, url_for,Blueprint, send_file
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename
from manejoBasesSQL import *
from reportRCA import *

UPLOAD_FOLDER = 'static/uploads/'
bibliotecaRegional_routes = Blueprint('bibliotecaRegional', __name__)
ruta=os.path.join(os.getcwd(), "base")
# Inicializar datos en la sesión
def initialize_data():
    if 'bibliotecaPlanta' not in session:
        session['bibliotecaRegional'] = {}
    if 'evento' not in session:
        session['evento'] = {}
    if 'equipo' not in session:
        session['equipo'] = {}
    if 'secuencias' not in session:
        session['secuencias'] = []
    if 'condiciones' not in session:
        session['condiciones'] = []
    if 'problema' not in session:
        session['problema'] = {}
    if 'fenomeno' not in session:
        session['fenomeno'] = {}
    if 'cincoporque' not in session:
        session['cincoporque'] = {}
    if 'contramedidas' not in session:
        session['contramedidas'] = []
    if 'imagen_averia' not in session:
        session['imagen_averia']=[]


def lecturaBase(nombreBase,index):
    nombre=os.path.join(ruta, nombreBase)
    try:
        with open(nombre, "r", encoding="utf-8") as file:
            df = pd.read_csv(file, sep="\t")
            df_show = df[df["Evento"] == index]
            return df_show, df
    except KeyError:
        print("Falla extracción")



@bibliotecaRegional_routes.route('/bibliotecaRegional', methods=['GET','POST'])
@login_required
def bibliotecaRegional():
    session['bibliotecaregional'] = True
    session.pop('bibliotecausuario', None)
    data, usuario_actual, datarow, planta_actual = read_data_usuario()
    data = data.to_dict(orient="records")
    titulo=f'Biblioteca Regional'
    return render_template("bibliotecaRegionalRCA.html", data=data, usuario_actual=usuario_actual,titulo=titulo)

@bibliotecaRegional_routes.route("/", methods=["GET", "POST"])
@login_required
def read_data_usuario():
    usuario_actual = current_user.username
    planta_actual=current_user.plant
    nombre_tabla = "evento"
    imagen_predeterminada= "/static/images/Pepsico_logo_blanco.png"  # Nombre de la tabla en la base de datos

    try:
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect(db_path)
        
        # Leer todos los datos de la tabla
        query = f"SELECT * FROM {nombre_tabla}"
        df = pd.read_sql_query(query, conn)

        # Validar si las columnas necesarias existen
        columnas_predeterminadas = ["ID","Titulo","Autor","Area_Empresa","OT_Averia" ,"Fecha_Evento", "Linea_Produccion", "Categoria","Planta","Aprobado","Terminado","Aprobado_Regional"]
        columnas_existentes = [col for col in columnas_predeterminadas if col in df.columns]
        
        if not columnas_existentes:
            raise KeyError(f"No se encontraron las columnas necesarias en la tabla {nombre_tabla}.")
        # Filtrar datos por el usuario actual y por las condiciones adicionales
        df_show = df[ (df["Aprobado"] == True) & (df["Terminado"] == True)&(df["Aprobado_Regional"] == True)][columnas_existentes]


        query_equipo = "SELECT Evento, Imagen FROM equipo"
        df_equipo = pd.read_sql_query(query_equipo, conn)

        # Unir las dos tablas por la columna 'evento' en equipo y 'ID' en evento
        df_show = pd.merge(df_show, df_equipo, left_on="ID", right_on="Evento", how="left")
        df_show['Imagen'] = df_show['Imagen'].fillna(imagen_predeterminada)



        # Cerrar la conexión
        conn.close()

        # Retornar DataFrames
        return df_show, usuario_actual, df, planta_actual

    except sqlite3.OperationalError as e:
        print(f"Error de operación en la base de datos: {str(e)}")
        return None, usuario_actual, pd.DataFrame(),planta_actual  # DataFrame vacío en caso de error
    
    except KeyError as e:
        print(f"Error de columnas: {str(e)}")
        return None, usuario_actual, pd.DataFrame(),planta_actual  # DataFrame vacío en caso de columnas faltantes
    
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None, usuario_actual, pd.DataFrame(),planta_actual  # DataFrame vacío en caso de error



@bibliotecaRegional_routes.route('/select/<int:index>')
@login_required
def select(index):
    initialize_data()

    # Cargar datos del evento
    if not cargarDatoID("evento", "ID", index):
        print("No se encontró el evento.")
        return redirect(url_for("bibliotecaRegional.bibliotecaRegional"))
    session['evento']['ID'] = index
    print(session['evento'])

    # Cargar problema relacionado
    if not cargarDatoID("problema", "Evento", index):
        print("No se encontró el problema relacionado.")
        session['problema'] = {}  # Vaciar problema en sesión
    
    if not cargarDatoID("fenomeno", "Evento", index):
        print("No se encontró el fenomeno relacionado.")
        session['fenomeno'] = {}

    if not cargarDatoID("equipo", "Evento", index):
        print("No se encontró el equipo relacionado.")
        session['equipo'] = {}

    if not cargarDatoID("cincoporque", "Evento", index):
        print("No se encontró el cincoporque relacionado.")
        session['cincoporque'] = {}

    if not cargarDatosLista("condiciones", "Evento", index):
        print("No se encontró las condiciones relacionado.")
        session['condiciones'] = []
    
    if not cargarDatosLista("secuencia", "Evento", index):
        print("No se encontró la secuencia relacionado.")
        session['secuencia'] = []

    if not cargarDatosLista("contramedidas", "Evento", index):
        print("No se encontró las contramedidas relacionado.")
        session['contramedidas'] = []

    if not cargarDatosLista("imagen_averia", "Evento", index):
        print("No se encontró las imagen de avería relacionada.")
        session['imagen_averia'] = []
    return redirect(url_for("evento.evento"))

    

@bibliotecaRegional_routes.route('/reporte/<int:index>')
@login_required
def reporte(index):
    initialize_data()

    # Cargar datos del evento
    if not cargarDatoID("evento", "ID", index):
        print("No se encontró el evento.")
        return redirect(url_for("bibliotecaRegional.bibliotecaRegional"))
    session['evento']['ID'] = index
    print(session['evento'])

    # Cargar problema relacionado
    if not cargarDatoID("problema", "Evento", index):
        print("No se encontró el problema relacionado.")
        session['problema'] = {}  # Vaciar problema en sesión
    
    if not cargarDatoID("fenomeno", "Evento", index):
        print("No se encontró el fenomeno relacionado.")
        session['fenomeno'] = {}

    if not cargarDatoID("equipo", "Evento", index):
        print("No se encontró el equipo relacionado.")
        session['equipo'] = {}

    if not cargarDatoID("cincoporque", "Evento", index):
        print("No se encontró el cincoporque relacionado.")
        session['cincoporque'] = {}

    if not cargarDatosLista("condiciones", "Evento", index):
        print("No se encontró las condiciones relacionado.")
        session['condiciones'] = []
    
    if not cargarDatosLista("secuencia", "Evento", index):
        print("No se encontró la secuencia relacionado.")
        session['secuencia'] = []

    if not cargarDatosLista("contramedidas", "Evento", index):
        print("No se encontró las constramedidas relacionado.")
        session['contramedidas'] = []

    if not cargarDatosLista("imagen_averia", "Evento", index):
        print("No se encontró las imagen de avería relacionada.")
        session['imagen_averia'] = []

    return render_template("Impresion.html", session=session)
    



@bibliotecaRegional_routes.route('/delete', methods=['POST'])
@login_required
def delete():
    # Obtener el ID del formulario enviado desde el frontend
    delete_id = request.form.get('deleteId')
    
    if not delete_id:
        flash("No se recibió un ID válido para eliminar.", "danger")
        return redirect(url_for('bibliotecaRegional.bibliotecaRegional'))

    try:
        # Llamar a la función genérica para eliminar el registro
        if eliminarFilaPorColumna("evento", "ID", delete_id):
            
            return redirect(url_for('bibliotecaRegional.bibliotecaRegional'))
            #flash("Registro eliminado con éxito.", "success")
        else:
            return redirect(url_for('bibliotecaRegional.bibliotecaRegional'))
            #flash("No se encontró el registro para eliminar.", "warning")

    except Exception as e:
        flash(f"Error al eliminar el registro: {str(e)}", "danger")

    return redirect(url_for('bibliotecaRegional.bibliotecaRegional'))

@bibliotecaRegional_routes.route('/download_report')
def download_report():
    # Example data
    data = session

    # Generate PDF in memory
    pdf_buffer = generate_pdf(data, "analysis_report.pdf")
    
    # Send the generated PDF as a downloadable file
    return send_file(pdf_buffer, as_attachment=True, download_name="report.pdf", mimetype="application/pdf")
