from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import bcrypt
import os 
import sqlite3

from auth_config import login_manager
from manejoBasesSQL import *

UPLOAD_FOLDER = 'static/uploads/'
login_routes = Blueprint('login', __name__)
ruta = os.path.join(os.getcwd(), "base")
db_path = os.path.join(ruta, "base.db")
db_route = os.path.join(ruta, "init_db.sql")

# CREACIÓN DE CLASE DE OBJETO USUARIO 
class User(UserMixin):
    def __init__(self, username, position, country, plant, first_name, last_name, sap_position, email, pending_approval):
        self.id = username  # Este es el identificador único del usuario
        self.username = username
        self.position = position
        self.country = country
        self.plant = plant
        self.firstName = first_name
        self.lastName = last_name
        self.sapPosition = sap_position
        self.email = email
        self.pending_approval = pending_approval

    def get_id(self):
        return self.username  # El método get_id debe retornar el `username` (no el `id`)

@login_manager.user_loader
def load_user(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #print(f'Intentando cargar el usuario: {username}')

    # Buscar los datos del usuario en la base de datos
    query = "SELECT * FROM usuarios WHERE username = ?"
    cursor.execute(query, (username,))
    row = cursor.fetchone()  # Obtiene una única fila
    conn.close()

    if row:
        # Crear el objeto User con los datos obtenidos de la base de datos
        user = User(
            username=row[1],
            position=row[6],
            country=row[7],
            plant=row[8],
            first_name=row[4],
            last_name=row[5],
            sap_position=row[10],
            email=row[3],
            pending_approval=bool(row[11])
        )
        #print(f'Intentando cargar el usuario: {user.pending_approval}')

        return user
    
    return None

@login_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        country = request.form['country']
        plant = request.form['plant']
        phone = request.form['phone']
        sap_position = request.form['sap_position']

        # Conexión a la base de datos para verificar si el usuario ya existe
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si el nombre de usuario ya existe en la base
        cursor.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,))
        user_exists = cursor.fetchone()  # None si no existe, 1 si existe

        if user_exists:
            flash('El nombre de usuario ya existe. Por favor elige otro.', 'warning')
            conn.close()
            return redirect(url_for('login.register'))

        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insertar el nuevo usuario en la base de datos
        cursor.execute("""
            INSERT INTO usuarios (username, password, email, first_name, last_name, position, country, plant, phone, sap_position, pending_approval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, hashed_password, email, first_name, last_name, position, country, plant, phone, sap_position, False))

        conn.commit()
        conn.close()
        

        flash(f'Usuario registrado con éxito', 'success')
        return redirect(url_for('login.register'))

    return render_template('register.html')


@login_routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Conexión a la base de datos para buscar al usuario
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Consultar si el usuario existe y obtener sus datos
        cursor.execute("""
            SELECT username, password, position, country, plant, first_name, last_name, sap_position, email, pending_approval
            FROM usuarios
            WHERE username = ?
        """, (username,))
        user_data = cursor.fetchone()  # Retorna None si el usuario no existe

        conn.close()

        if user_data:
            stored_password = user_data[1]  # Segunda columna: contraseña encriptada

            # Verificar si la contraseña es correcta
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # Crear objeto `User` con los datos del usuario
                user = User(
                    username=user_data[0],
                    position=user_data[2],
                    country=user_data[3],
                    plant=user_data[4],
                    first_name=user_data[5],
                    last_name=user_data[6],
                    sap_position=user_data[7],
                    email=user_data[8],
                    pending_approval=bool(user_data[9])
                )
                login_user(user)  # Iniciar sesión con Flask-Login

                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('login.welcome'))
            else:
                flash('Contraseña incorrecta. Intenta nuevamente.', 'warning')
        else:
            flash('El usuario no existe.', 'warning')

    return render_template('login.html')


@login_routes.route('/logout')
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario
    flash('Has cerrado sesión', 'success')  # Muestra un mensaje de éxito
    return redirect(url_for('login.login'))  # Redirige a la página de inicio de sesión

@login_routes.route('/welcome')
@login_required
def welcome():
    session.pop('evento', None)
    session.pop('equipo', None)
    session.pop('secuencia', None)
    session.pop('condiciones', None)
    session.pop('problema', None)
    session.pop('fenomeno', None)
    session.pop('cincoporque', None)
    session.pop('contramedidas', None)
    session.pop('imagen_averia', None)
    limpiar_carpeta_temporal(current_user.username)

    return render_template('newHomeView.html', current_user=current_user)


@login_routes.route('/edit_user/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    # Verificación del valor del parámetro 'username'
    print(f"Editando usuario: {username}")

    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Buscar al usuario en la base de datos
    cursor.execute("""
        SELECT username, first_name, last_name, email, position, country, plant, phone, sap_position, pending_approval
        FROM usuarios
        WHERE username = ?
    """, (username,))
    
    user_data = cursor.fetchone()

    # Verificación si el usuario existe
    if not user_data:
        print('Usuario no encontrado.')
        conn.close()  # Cierra la conexión si no se encuentra el usuario
        flash('Usuario no encontrado.', 'warning')  # Mensaje de error en la UI
        return redirect(url_for('login.welcome'))  # Redirige al inicio si no se encuentra el usuario

    # Mapea los datos de la base de datos a un diccionario
    user = {
        'username': user_data[0],
        'first_name': user_data[1],
        'last_name': user_data[2],
        'email': user_data[3],
        'position': user_data[4],
        'country': user_data[5],
        'plant': user_data[6],
        'phone': user_data[7],
        'sap_position': user_data[8],
        'pending_approval': bool(user_data[9]),
    }
    
    # Si la solicitud es POST, actualizar los datos del usuario
    if request.method == 'POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_email = request.form['email']
        new_position = request.form['position']
        new_country = request.form['country']
        new_plant = request.form['plant']
        new_phone = request.form['phone']
        new_sap_position = request.form['sap_position']

        # Verifica si la posición ha cambiado y ajusta el estado de aprobación
        if user['position'] != new_position:
            user['pending_approval'] = True

        # Actualiza los datos del usuario en la base de datos
        cursor.execute("""
            UPDATE usuarios 
            SET first_name = ?, last_name = ?, email = ?, position = ?, country = ?, plant = ?, phone = ?, sap_position = ?, pending_approval = ?
            WHERE username = ?
        """, (new_first_name, new_last_name, new_email, new_position, new_country, new_plant, new_phone, new_sap_position, user['pending_approval'], username))

        conn.commit()
        conn.close()

        # Muestra mensaje de éxito y redirige
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('login.welcome'))

    conn.close()  # Asegúrate de cerrar la conexión al final

    # Si el método es GET, renderiza el formulario con los datos del usuario
    return render_template('edit_user.html', user=user)

