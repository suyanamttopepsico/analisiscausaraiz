from flask import Flask, render_template, request, session, redirect, url_for,Blueprint
from datetime import datetime
import uuid
from flask_login import current_user,login_required
import pandas as pd
import os
from werkzeug.utils import secure_filename
from manejoBasesSQL import *
from reportRCA import *

UPLOAD_FOLDER = 'static/uploads/'
bibliotecaPersonal_routes = Blueprint('bibliotecaPersonal', __name__)
ruta=os.path.join(os.getcwd(), "base")
# Inicializar datos en la sesión
def initialize_data():
    if 'bibliotecaPersonal' not in session:
        session['bibliotecaPersonal'] = {}
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
def title_case_paragraphs(text):
    # Dividir el texto en párrafos usando el salto de línea como delimitador
    paragraphs = text.split('\n')
    
    # Convertir cada palabra de cada párrafo a título
    title_case_paragraphs = [paragraph.title() for paragraph in paragraphs]
    
    # Unir los párrafos de nuevo en un solo string
    title_case_text = '\n'.join(title_case_paragraphs)
    
    return title_case_text

def obtener_nombre_completo(db_path, username):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ejecutar la consulta
        query = "SELECT first_name, last_name FROM usuarios WHERE username = ?"
        cursor.execute(query, (username,))
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        # Cerrar la conexión
        conn.close()
        
        if resultado:
            return resultado
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


""" # Ruta principal para ingresar el equipo
@bibliotecaPersonal_routes.route("/", methods=["GET", "POST"])
@login_required
def read_data_usuario():
    usuario_actual = current_user.username
    nombreBase=os.path.join(ruta, "evento.txt")
    try:
        with open(nombreBase, "r", encoding="utf-8") as file:
            df = pd.read_csv(file, sep="\t")
            columns_to_display = ["ID","Autor","Causa RCA",'Categoria']
            #print("Se lee el df")
            df_show = df[df["Autor"] == usuario_actual][columns_to_display]
            #print("Se filtra")
            #print(df)
            return df_show, usuario_actual, df
    except KeyError:
        print("No se filtra")
        print("Algunas columnas no existen. Mostrando todas las columnas.")
        with open(nombreBase, "r", encoding="utf-8") as file:
            df = pd.read_csv(file)
            columns_to_display = ["ID",'Autor', 'Fecha Evento','Categoria']
            df_show = df
            return df_show, usuario_actual, df
    
 """

@bibliotecaPersonal_routes.route('/bibliotecausuario', methods=['GET','POST'])
@login_required
def bibliotecausuario():
    session['bibliotecausuario'] = True
    session.pop('bibliotecaPlanta', None)
    data, usuario_actual, datarow = read_data_usuario()
    data = data.to_dict(orient="records")
    name=obtener_nombre_completo(db_path, usuario_actual)
    titulo=f'Biblioteca de {title_case_paragraphs(name[0])}'
    return render_template("bibliotecapersonalRCA.html", data=data, usuario_actual=usuario_actual,titulo=titulo)

@bibliotecaPersonal_routes.route("/", methods=["GET", "POST"])
@login_required
def read_data_usuario():
    usuario_actual = current_user.username
    nombre_tabla = "evento"
    imagen_predeterminada= "/static/images/Pepsico_logo_blanco.png"  # Nombre de la tabla en la base de datos

    try:
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect(db_path)
        
        # Leer todos los datos de la tabla
        query = f"SELECT * FROM {nombre_tabla}"
        df = pd.read_sql_query(query, conn)

        # Validar si las columnas necesarias existen
        columnas_predeterminadas = ["ID","Titulo","Autor","Area_Empresa","OT_Averia" ,"Fecha_Evento", "Linea_Produccion", "Categoria"]
        columnas_existentes = [col for col in columnas_predeterminadas if col in df.columns]
        
        if not columnas_existentes:
            raise KeyError(f"No se encontraron las columnas necesarias en la tabla {nombre_tabla}.")

        # Filtrar datos por el usuario actual
        df_show = df[df["Autor"] == usuario_actual][columnas_existentes]

                # Filtrar datos por el usuario actual
        # Leer datos de la tabla equipo
        query_equipo = "SELECT Evento, Imagen FROM equipo"
        df_equipo = pd.read_sql_query(query_equipo, conn)

        # Unir las dos tablas por la columna 'evento' en equipo y 'ID' en evento
        df_show = pd.merge(df_show, df_equipo, left_on="ID", right_on="Evento", how="left")

                # Asignar imagen predeterminada si la ruta de la imagen está vacía
        df_show['Imagen'] = df_show['Imagen'].fillna(imagen_predeterminada)

        print(df_show)

        # Cerrar la conexión
        conn.close()


        # Cerrar la conexión
        conn.close()

        # Retornar DataFrames
        return df_show, usuario_actual, df

    except sqlite3.OperationalError as e:
        print(f"Error de operación en la base de datos: {str(e)}")
        return None, usuario_actual, pd.DataFrame()  # DataFrame vacío en caso de error
    
    except KeyError as e:
        print(f"Error de columnas: {str(e)}")
        return None, usuario_actual, pd.DataFrame()  # DataFrame vacío en caso de columnas faltantes
    
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None, usuario_actual, pd.DataFrame()  # DataFrame vacío en caso de error



@bibliotecaPersonal_routes.route('/select/<int:index>')
@login_required
def select(index):
    initialize_data()

    # Cargar datos del evento
    if not cargarDatoID("evento", "ID", index):
        print("No se encontró el evento.")
        return redirect(url_for("bibliotecaPersonal.bibliotecausuario"))
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

    

@bibliotecaPersonal_routes.route('/reporte/<int:index>')
@login_required
def reporte(index):
    initialize_data()

    # Cargar datos del evento
    if not cargarDatoID("evento", "ID", index):
        print("No se encontró el evento.")
        return redirect(url_for("bibliotecaPersonal.bibliotecausuario"))
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

    return download_report()
"""
@bibliotecaPersonal_routes.route('/select/<int:index>')
@login_required
def select(index):
    if session.get('bibliotecausuario'):
        data, _ ,full_data = read_data_usuario()
    else:
        flash("No hay biblioteca activa en la sesión.")
        return redirect(url_for("login.welcome"))

    initialize_data()
    session['evento'] = full_data[full_data["ID"]==index].to_dict(orient='records')[0]
    problema,_=lecturaBase("problema.txt",index)
    #----PENDIENTE CREAR EL INDICE Y LA CARGA DE LOS DEMÁS EVENTOS
    #session['problema'] = problemaBase[full_data["ID"]==index].to_dict(orient='records')[0]
    print(problema)    
    return redirect(url_for("evento.evento")) """



"""@bibliotecaPersonal_routes.route('/delete', methods=['POST'])
@login_required
def delete():
    index = request.form.get('deleteId')  # Obtener el índice del formulario
    if index:
        index = int(index)  # Convertir a entero si es necesario
        
        # Archivos a eliminar
        archivos = ['eventos.txt', 'problemas.txt', 'secuencias.txt']
        # Ruta base donde se encuentran los archivos
        ruta = os.path.join(os.getcwd(), 'bases')
        nombreBase=os.path.join(ruta, "evento.txt")

        try:
            if session.get('bibliotecausuario'):
                data, _ ,full_data = read_data_usuario()
            else:
                print("No hay biblioteca activa en la sesión.")
                return redirect(url_for("login.welcome"))

            if 0 <= index < len(full_data):
                full_data = full_data.drop(full_data.index[index]).reset_index(drop=True)
                full_data.to_csv(nombreBase, sep="\t", index=False)
                print("Registro eliminado con éxito.")
            else:
                print("Índice fuera de rango.")
        except Exception as e:
            print(f"Error al eliminar los archivos: {str(e)}", "danger")
    
    return redirect(url_for("bibliotecaPersonal.bibliotecausuario"))"""


@bibliotecaPersonal_routes.route('/delete', methods=['POST'])
@login_required
def delete():
    # Obtener el ID del formulario enviado desde el frontend
    delete_id = request.form.get('deleteId')
    
    if not delete_id:
        flash("No se recibió un ID válido para eliminar.", "danger")
        return redirect(url_for('bibliotecaPersonal.bibliotecausuario'))

    try:
        # Llamar a la función genérica para eliminar el registro
        if eliminarFilaPorColumna("evento", "ID", delete_id):

            return redirect(url_for('bibliotecaPersonal.bibliotecausuario'))
            #flash("Registro eliminado con éxito.", "success")
        else:
            return redirect(url_for('bibliotecaPersonal.bibliotecausuario'))
            #flash("No se encontró el registro para eliminar.", "warning")

    except Exception as e:
        flash(f"Error al eliminar el registro: {str(e)}", "danger")

    return redirect(url_for('bibliotecaPersonal.bibliotecausuario'))




""" # Ruta para eliminar un registro
@bibliotecaPersonal_routes.route('/eliminar/<int:index>', methods=['POST'])
def eliminar(index):
    data, _ ,full_data = read_data_usuario()
    datos = full_data.drop(index) 
    nombreBase=os.path.join(ruta, "evento.txt") # Eliminar el registro según el índice
    datos.to_csv(nombreBase, index=False, sep="\t")  # Guardar el DataFrame actualizado en el archivo
    return redirect(url_for('bibliotecaPersonal.bibliotecausuario'))  # Redirigir a la página principal de la tabla """

@bibliotecaPersonal_routes.route('/download_report')
def download_report():
    # Example data
    # Example data (you can replace this with actual data)
    data = session

    # Generate PDF in memory
    pdf_buffer = generate_pdf(data, "analysis_report.pdf")
    
    # Send the generated PDF as a downloadable file
    return send_file(pdf_buffer, as_attachment=True, download_name="report.pdf", mimetype="application/pdf")
