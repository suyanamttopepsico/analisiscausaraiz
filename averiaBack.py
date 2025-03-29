from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'
# Inicializamos el DataFrame
if os.path.exists("condiciones.csv"):
    df_condiciones = pd.read_csv("condiciones.csv")
else:
    df_condiciones = pd.DataFrame(columns=["descripcion", "imagen"])

# Nombre de la base
filename = 'averiaBase.txt'



###############################################################################
# Función para leer o crear la base de datos
def lecturaBase():
    if os.path.exists(filename):
        df = pd.read_csv(filename, sep="\t") 
    else:
        # Crear DataFrame vacío con columnas definidas
        df = pd.DataFrame(columns=["ID", "Categoria", "Fecha Evento", "OT Avería", "OT RCA", "Planta", 
                                   "Línea Producción", "Área Empresa", "Cod SAP", "Nombre Equipo SAP",
                                   "Causa RCA", "Costos", "Tiempo Total", "Técnico", 
                                   "Representante Mantenimiento", "Representante SASS", "Representante Calidad", 
                                   "Representante Producción"])
        df.to_csv(filename, sep="\t", index=False)
    return df

###############################################################################
# Función para agregar una fila a la base de datos
def agregarFila(data):
    df = lecturaBase()
    
    # Asignar el ID a la nueva fila
    if len(df) == 0:
        ID = 1
    else:
        ID = df["ID"].max() + 1  
    
    # Añadir el número al diccionario de datos
    data['ID'] = ID
    
    # Concatenar los datos nuevos con los existentes
    aux = pd.DataFrame([data])
    dfR = pd.concat([df, aux], ignore_index=True)
    
    # Guardar el DataFrame actualizado
    dfR.to_csv(filename, sep="\t", index=False)
###############################################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/step1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        # Guardar los datos de las tres entradas en la sesión
        session['datos'] = {
            'Categoria': request.form.get('categoria'),
            'Fecha Evento': request.form.get('fechaEvento'),
            'OT Avería': request.form.get('otAveria'),
            'OT RCA': request.form.get('otRca'),
            'Planta': request.form.get('planta'),
            'Línea Producción': request.form.get('lineaProduccion'),
            'Área Empresa': request.form.get('areaEmpresa'),
            'Cod SAP': request.form.get('codigoSap'),
            'Nombre Equipo SAP': request.form.get('nombreEquipo'),
            'Causa RCA': request.form.get('causaRca'),
            'Costos': request.form.get('costos'),
            'Tiempo Total': request.form.get('tiempoTotal'),
            'Técnico': request.form.get('tecnicoEvento'),
            'Representante Mantenimiento': request.form.get('representanteMantenimiento'),
            'Representante SASS': request.form.get('representanteSass'),
            'Representante Calidad': request.form.get('representanteCalidad'),
            'Representante Producción': request.form.get('representanteProduccion')
        }
        if request.form['action'] == 'index':
            return redirect(url_for('index'))
        elif request.form['action'] == 'step2':
            return redirect(url_for('equipo'))

    return render_template('evento.html', datos=session.get('datos', {}))

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        
        if request.form['action'] == 'index': 
            agregarFila(session["datos"])
            session['datos'] = {}
            
            return redirect(url_for('index'))
        
        elif request.form['action'] == 'step1':
            return redirect(url_for('step1'))
            
    return render_template('step2.html')

@app.route('/guardar_sesion', methods=['POST'])
def guardar_sesion():
    datos = request.json.get('datos', [])
    session['secuencias'] = datos
    return jsonify({'success': True})

@app.route('/equipo', methods=['GET', 'POST'])
def equipo():
   if request.method == 'POST':
        # Obtener las secuencias del formulario
        session["equipo"]={
            'Equipo': request.form.get('equipo'),
            'Fabricante': request.form.get('fabricante')
            }

        session["secuencias"] = request.form.getlist('secuencia_texto[]')
        
        if request.form.get('action') == 'index': 
            return redirect(url_for('index'))
        
        elif request.form.get('action') == 'step1':
            return redirect(url_for('step1'))
        
   secuencias = session.get('secuencias', [])

   return render_template('equipo.html', secuencias=secuencias, equipo=session.get('equipo', {}))

@app.route('/condiciones', methods=['GET', 'POST'])
def condiciones():
    global df_condiciones

    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')

        if descripcion and imagen:
            ruta_imagen = f'static/uploads/{imagen.filename}'
            imagen.save(ruta_imagen)

            # Agregar nueva fila al DataFrame usando pd.concat
            nueva_condicion = pd.DataFrame({"descripcion": [descripcion], "imagen": [ruta_imagen]})
            df_condiciones = pd.concat([df_condiciones, nueva_condicion], ignore_index=True)
            df_condiciones.to_csv("condiciones.csv", index=False)  # Guardar a disco

        return jsonify(success=True)

    # Renderizar HTML en la primera carga (GET)
    return render_template('condicionesQ1.html')

@app.route('/cargar_condiciones', methods=['GET'])
def cargar_condiciones():
    # Convertir el DataFrame a JSON para enviarlo al frontend
    return jsonify(condiciones=df_condiciones.to_dict(orient="records"))

@app.route('/eliminar_condicion/<int:index>', methods=['DELETE'])
def eliminar_condicion(index):
    global df_condiciones

    if index < len(df_condiciones):
        df_condiciones = df_condiciones.drop(index).reset_index(drop=True)
        df_condiciones.to_csv("condiciones.csv", index=False)  # Guardar a disco

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)

