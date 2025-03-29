
#Importación de librerias
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import bcrypt
import os 
from werkzeug.utils import secure_filename

#Importación de archivos 
from bases_routes import bases_routes
from evento_routes import evento_routes
from equipo_routes import equipo_routes
from condiciones_routes import condiciones_routes
from problema_routes import problema_routes
from fenomeno_routes import fenomeno_routes
from cincoporque_routes import cincoporque_routes
from contramedidas_routes import contramedidas_routes
from bibliotecaPersonal_routes import bibliotecaPersonal_routes
from bibliotecaPlanta_routes import bibliotecaPlanta_routes
from bibliotecaAprobado_routes import bibliotecaAprobado_routes
from bibliotecaRegional_routes import bibliotecaRegional_routes
from asignado_routes import asignado_routes
from auth_config import login_manager
from login_routes import User,load_user,login_routes

app = Flask(__name__)
app.secret_key = "supersecretkey"
login_manager.init_app(app)  
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Registrar rutas
app.register_blueprint(bases_routes, url_prefix='/bases')
app.register_blueprint(evento_routes, url_prefix='/evento')
app.register_blueprint(equipo_routes, url_prefix='/equipo')
app.register_blueprint(condiciones_routes, url_prefix='/condiciones')
app.register_blueprint(problema_routes, url_prefix='/problema')
app.register_blueprint(fenomeno_routes, url_prefix='/fenomeno')
app.register_blueprint(cincoporque_routes, url_prefix='/cincoporque')
app.register_blueprint(contramedidas_routes, url_prefix='/contramedidas')
app.register_blueprint(login_routes, url_prefix='/auth')
app.register_blueprint(bibliotecaPersonal_routes, url_prefix='/bibliotecapersonalRCA')
app.register_blueprint(bibliotecaPlanta_routes, url_prefix='/bibliotecaPlantaRCA')
app.register_blueprint(bibliotecaAprobado_routes, url_prefix='/bibliotecaAprobadoRCA')
app.register_blueprint(bibliotecaRegional_routes, url_prefix='/bibliotecaRegionalRCA')
app.register_blueprint(asignado_routes, url_prefix='/asignado')
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)

