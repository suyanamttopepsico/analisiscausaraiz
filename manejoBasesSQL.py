from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from flask_login import current_user,login_required
#from werkzeug.utils import secure_filename
import pandas as pd
import os
import sqlite3
import glob

ruta = os.path.join(os.getcwd(), "base")
os.makedirs(ruta, exist_ok=True)  # Crea el directorio si no existe

db_path = os.path.join(ruta, "base.db")
db_route = os.path.join(ruta, "init_db.sql")

FINAL_UPLOAD_FOLDER = 'static/uploads/final/'
TEMP_UPLOAD_FOLDER = 'static/uploads/temp/'

def get_user_temp_folder(username):
    """Crea una carpeta temporal para el usuario si no existe."""
    user_folder = os.path.join(TEMP_UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder


def limpiar_carpeta_temporal(username):
    """Elimina todos los archivos en la carpeta temporal de un usuario."""
    user_temp_folder = get_user_temp_folder(username)
    for file in os.listdir(user_temp_folder):
        os.remove(os.path.join(user_temp_folder, file))

def get_event_folder(event_id):
    """Crea una carpeta específica para el evento si no existe."""
    event_folder = os.path.join(FINAL_UPLOAD_FOLDER, f"evento_{event_id}")
    os.makedirs(event_folder, exist_ok=True)
    return event_folder


# Llama a esta función al iniciar la aplicación o al abandonar una pantalla

def move_images_to_final(namesession,eventoID, username,columnasession='Imagen_de_Averia'):
    """
    Mueve imágenes desde la carpeta temporal del usuario a la carpeta final del evento.
    Actualiza las rutas en session['problema']['Imagen_de_Averia'].
    """
    imagenes_finales = []
    
    # Carpeta temporal del usuario
    user_temp_folder = get_user_temp_folder(username)
    
    # Carpeta final del evento
    event_folder = get_event_folder(eventoID)
    
    # Obtener las imágenes de la sesión
    imagenes_temporales = session[namesession]
    
    for img_data in imagenes_temporales:
        temp_path = img_data.get('Imagen_de_Averia', '')
        
            # Verificar que temp_path no sea None
        if temp_path is None:
            # Si es None, no hacer nada y terminar la función
            return
        if temp_path.startswith(f"/{user_temp_folder}"):
            temp_full_path = temp_path[1:]  # Quitar la barra inicial '/'
            filename = os.path.basename(temp_full_path)
            
            # Crear ruta final
            final_path = os.path.join(event_folder, filename)
            
            # Mover la imagen
            os.rename(temp_full_path, final_path)
            
            # Actualizar la lista con la nueva ruta
            imagenes_finales.append({
                'Imagen_de_Averia': f"/{final_path}",
                'Indice': img_data.get('Indice', len(imagenes_finales) + 1)
            })
        else:
            # Si la imagen no está en la carpeta temporal, mantenerla como está
            imagenes_finales.append(img_data)
    
    # Actualizar las rutas en la sesión
    session[namesession]= imagenes_finales


def move_image_to_final(namesession, eventoID, username, columnasession="Imagen"):
    imagenes_finales = ""

    # Verificar si namesession existe en session
    if namesession not in session:
        #raise KeyError(f"'{namesession}' no está en la sesión.")
        return

    # Verificar si columnasession existe en namesession
    if columnasession not in session[namesession]:
        #raise KeyError(f"'{columnasession}' no está en 'session[{namesession}]'.")
        return

    # Carpeta temporal del usuario
    user_temp_folder = get_user_temp_folder(username)
    
    # Carpeta final del evento
    event_folder = get_event_folder(eventoID)
    
    # Obtener las imágenes de la sesión
    temp_path = session[namesession][columnasession]

        # Verificar que temp_path no sea None
    if temp_path is None:
        # Si es None, no hacer nada y terminar la función
        return

    if temp_path.startswith(f"/{user_temp_folder}"):
        temp_full_path = temp_path[1:]  # Quitar la barra inicial '/'
        filename = os.path.basename(temp_full_path)
        
        # Crear ruta final
        final_path = os.path.join(event_folder, filename)
        
        # Mover la imagen
        os.rename(temp_full_path, final_path)
        
        # Actualizar la lista con la nueva ruta
        imagenes_finales = f"/{final_path}"
    else:
        # Si la imagen no está en la carpeta temporal, mantenerla como está
        imagenes_finales=temp_path

    # Actualizar la sesión
    session[namesession][columnasession] = imagenes_finales


def move_image_to_final_condiciones(namesession, eventoID, username, columnasession="Imagen"):
    imagenes_finales = ""

    # Verificar si namesession existe en session
    if namesession not in session:
        #raise KeyError(f"'{namesession}' no está en la sesión.")
        return

    # Carpeta temporal del usuario
    user_temp_folder = get_user_temp_folder(username)
    
    # Carpeta final del evento
    event_folder = get_event_folder(eventoID)
    
    for imagen in session[namesession]:
        # Verificar si columnasession existe en la imagen
        if columnasession not in imagen:
            raise KeyError(f"'{columnasession}' no está en la imagen.")

        # Obtener las imágenes de la sesión
        temp_path = imagen[columnasession]

            # Verificar que temp_path no sea None
        if temp_path is None:
            # Si es None, no hacer nada y terminar la función
            return

        if temp_path.startswith(f"/{user_temp_folder}"):
            temp_full_path = temp_path[1:]  # Quitar la barra inicial '/'
            filename = os.path.basename(temp_full_path)
            
            # Crear ruta final
            final_path = os.path.join(event_folder, filename)
            
            # Mover la imagen
            os.rename(temp_full_path, final_path)
            
            # Actualizar la lista con la nueva ruta
            imagenes_finales = f"/{final_path}"
        
        # Actualizar el valor de la clave
        imagen[columnasession] = imagenes_finales

    



# Crear la base de datos
def create_database():
    conn = sqlite3.connect(db_path)  # Asegúrate de que 'ruta' existe
    cursor = conn.cursor()
    with open(db_route, "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()


def init_database():
    # Verificar si existe la base de datos
    if not os.path.exists(db_path):
        #print("La base de datos no existe. Creándola...")
        create_database()
    else:
        return

# Crear la base de datos y las tablas
def initialize_database(bases):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for table, columns in bases.items():
        columns_str = ", ".join(columns)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
    conn.commit()
    conn.close()

# Función para almacenar los datos de un DataFrame en una base de datos SQL
def store_dataframe_in_db(db_path, df, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear la tabla si no existe
    if not cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'").fetchone():
        columns_str = ", ".join([f"{col} {dtype}" for col, dtype in zip(df.columns, df.dtypes)])
        cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")
    
    # Insertar los datos del DataFrame en la tabla
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()


# Leer registros de una tabla
def lecturaBase(base):
    init_database()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {base}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns

# # Agregar una fila con generación automática de ID
# def agregarFilaID(data, base):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     columns = ", ".join(data.keys())
#     placeholders = ", ".join(["?"] * len(data))
#     values = tuple(data.values())

#     cursor.execute(f"INSERT INTO {base} ({columns}) VALUES ({placeholders})", values)
#     conn.commit()
#     inserted_id = cursor.lastrowid
#     conn.close()
#     return inserted_id

# import sqlite3
def agregarFilaID(data, base):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verifica si ya existe un registro con el ID (puedes cambiar esto por otro campo único si es necesario)
    id = data.get("ID")  # Asegúrate de que "id" esté en el diccionario de data
    cursor.execute(f"SELECT * FROM {base} WHERE ID = ?", (id,))
    existing_row = cursor.fetchone()
    print(data.keys())

    if existing_row:
        # Si existe, realiza un UPDATE
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values())
        cursor.execute(f"UPDATE {base} SET {set_clause} WHERE id = ?", values + (id,))
        conn.commit()
        conn.close()
        print("Datos actualizados.")
        return id  # Devuelve el ID del registro actualizado
    else:
        # Si no existe, realiza un INSERT
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        cursor.execute(f"INSERT INTO {base} ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        inserted_id = cursor.lastrowid  # Obtener el ID recién insertado
        conn.close()
        print(f"Nuevo registro insertado, ID: {inserted_id}")
        return inserted_id  # Devuelve el nuevo ID insertado

# def agregarFila(data, base, campo, campoValor):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     try:
#         for item in data:
#             # Asegúrate de que el campo esté presente en el diccionario
#             item[campo] = campoValor
            
#             # Verifica que todos los campos estén presentes en la base de datos
#             columns = ", ".join(item.keys())
#             placeholders = ", ".join(["?"] * len(item))
#             values = tuple(item.values())
            
#             # Verificar la estructura de la consulta
#             query = f"INSERT INTO {base} ({columns}) VALUES ({placeholders})"
            
#             # Imprime la consulta para depurar
#             print(f"Ejecutando consulta: {query}")
#             print(f"Valores: {values}")
            
#             # Ejecuta la inserción
#             cursor.execute(query, values)

#         # Commit después de todas las inserciones
#         conn.commit()

#     except sqlite3.Error as e:
#         # Si ocurre un error, imprime el error
#         print(f"Error al insertar los datos: {e}")

#     finally:
#         conn.close()


def agregarFila(data, base, campo, campoValor, indiceSecundario=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if indiceSecundario:
            # Lógica con índice secundario para actualizar, insertar y eliminar registros
            cursor.execute(f"SELECT {indiceSecundario} FROM {base} WHERE {campo} = ?", (campoValor,))
            db_items = {row[0] for row in cursor.fetchall()}  # Conjunto de valores únicos existentes en la base

            # Obtener los índices secundarios de los datos actuales
            data_items = {item[indiceSecundario] for item in data}

            # Identificar elementos a eliminar
            items_to_delete = db_items - data_items

            # Eliminar los elementos que ya no están en los datos
            for item in items_to_delete:
                cursor.execute(f"DELETE FROM {base} WHERE {campo} = ? AND {indiceSecundario} = ?", (campoValor, item))
                print(f"Elemento eliminado: {campo} = {campoValor}, {indiceSecundario} = {item}")

            # Insertar o actualizar elementos actuales
            for item in data:
                item[campo] = campoValor  # Agregar valor del campo padre
                where_clause = f"{campo} = ? AND {indiceSecundario} = ?"
                query_params = (campoValor, item[indiceSecundario])

                # Verificar existencia en la base
                cursor.execute(f"SELECT * FROM {base} WHERE {where_clause}", query_params)
                existing_row = cursor.fetchone()

                if existing_row:
                    # Actualizar
                    set_clause = ", ".join([f"{key} = ?" for key in item.keys()])
                    values = tuple(item.values())
                    cursor.execute(f"UPDATE {base} SET {set_clause} WHERE {where_clause}", values + query_params)
                    print(f"Datos actualizados para {campo} = {campoValor}, {indiceSecundario} = {item[indiceSecundario]}")
                else:
                    # Insertar
                    columns = ", ".join(item.keys())
                    placeholders = ", ".join(["?"] * len(item))
                    values = tuple(item.values())
                    cursor.execute(f"INSERT INTO {base} ({columns}) VALUES ({placeholders})", values)
                    print(f"Datos insertados para {campo} = {campoValor}, {indiceSecundario} = {item[indiceSecundario]}")
        else:
            # Lógica sin índice secundario: solo insertar o actualizar sin eliminar registros
            for item in data:
                item[campo] = campoValor  # Agregar valor del campo padre

                # Preparar consulta de inserción/actualización
                columns = ", ".join(item.keys())
                placeholders = ", ".join(["?"] * len(item))
                values = tuple(item.values())

                # Verificar existencia de datos idénticos
                cursor.execute(f"SELECT * FROM {base} WHERE {campo} = ?", (campoValor,))
                existing_row = cursor.fetchone()

                if existing_row:
                    # Actualizar
                    set_clause = ", ".join([f"{key} = ?" for key in item.keys()])
                    cursor.execute(f"UPDATE {base} SET {set_clause} WHERE {campo} = ?", values + (campoValor,))
                    print(f"Datos actualizados para {campo} = {campoValor}")
                else:
                    # Insertar
                    query = f"INSERT INTO {base} ({columns}) VALUES ({placeholders})"
                    cursor.execute(query, values)
                    print(f"Datos insertados para {campo} = {campoValor}")

        # Confirmar cambios en la base de datos
        conn.commit()
        

    except sqlite3.Error as e:
        print(f"Error al insertar o actualizar los datos: {e}")

    finally:
        conn.close()

# def agregarFila(data, base, campo, campoValor, indiceSecundario=None):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     ids_actualizados_o_insertados = []  # Lista para almacenar las IDs procesadas

#     try:
#         if indiceSecundario:
#             # Lógica con índice secundario para actualizar, insertar y eliminar registros
#             cursor.execute(f"SELECT {indiceSecundario} FROM {base} WHERE {campo} = ?", (campoValor,))
#             db_items = {row[0] for row in cursor.fetchall()}  # Conjunto de valores únicos existentes en la base

#             # Obtener los índices secundarios de los datos actuales
#             data_items = {item[indiceSecundario] for item in data}

#             # Identificar elementos a eliminar
#             items_to_delete = db_items - data_items

#             # Eliminar los elementos que ya no están en los datos
#             for item in items_to_delete:
#                 cursor.execute(f"DELETE FROM {base} WHERE {campo} = ? AND {indiceSecundario} = ?", (campoValor, item))
#                 print(f"Elemento eliminado: {campo} = {campoValor}, {indiceSecundario} = {item}")

#             # Insertar o actualizar elementos actuales
#             for item in data:
#                 item[campo] = campoValor  # Agregar valor del campo padre
#                 where_clause = f"{campo} = ? AND {indiceSecundario} = ?"
#                 query_params = (campoValor, item[indiceSecundario])

#                 # Verificar existencia en la base
#                 cursor.execute(f"SELECT ID FROM {base} WHERE {where_clause}", query_params)
#                 existing_row = cursor.fetchone()

#                 if existing_row:
#                     # Actualizar
#                     set_clause = ", ".join([f"{key} = ?" for key in item.keys()])
#                     values = tuple(item.values())
#                     cursor.execute(f"UPDATE {base} SET {set_clause} WHERE {where_clause}", values + query_params)
#                     print(f"Datos actualizados para {campo} = {campoValor}, {indiceSecundario} = {item[indiceSecundario]}")
#                     ids_actualizados_o_insertados.append(existing_row[0])  # Agregar ID actualizado
#                 else:
#                     # Insertar
#                     columns = ", ".join(item.keys())
#                     placeholders = ", ".join(["?"] * len(item))
#                     values = tuple(item.values())
#                     cursor.execute(f"INSERT INTO {base} ({columns}) VALUES ({placeholders})", values)
#                     inserted_id = cursor.lastrowid
#                     print(f"Datos insertados para {campo} = {campoValor}, {indiceSecundario} = {item[indiceSecundario]}")
#                     ids_actualizados_o_insertados.append(inserted_id)  # Agregar ID insertado
#         else:
#             # Lógica sin índice secundario: solo insertar o actualizar sin eliminar registros
#             for item in data:
#                 item[campo] = campoValor  # Agregar valor del campo padre

#                 # Preparar consulta de inserción/actualización
#                 columns = ", ".join(item.keys())
#                 placeholders = ", ".join(["?"] * len(item))
#                 values = tuple(item.values())

#                 # Verificar existencia de datos idénticos
#                 cursor.execute(f"SELECT ID FROM {base} WHERE {campo} = ?", (campoValor,))
#                 existing_row = cursor.fetchone()

#                 if existing_row:
#                     # Actualizar
#                     set_clause = ", ".join([f"{key} = ?" for key in item.keys()])
#                     cursor.execute(f"UPDATE {base} SET {set_clause} WHERE {campo} = ?", values + (campoValor,))
#                     print(f"Datos actualizados para {campo} = {campoValor}")
#                     ids_actualizados_o_insertados.append(existing_row[0])  # Agregar ID actualizado
#                 else:
#                     # Insertar
#                     query = f"INSERT INTO {base} ({columns}) VALUES ({placeholders})"
#                     cursor.execute(query, values)
#                     inserted_id = cursor.lastrowid
#                     print(f"Datos insertados para {campo} = {campoValor}")
#                     ids_actualizados_o_insertados.append(inserted_id)  # Agregar ID insertado

#         # Confirmar cambios en la base de datos
#         conn.commit()

#     except sqlite3.Error as e:
#         print(f"Error al insertar o actualizar los datos: {e}")

#     finally:
#         conn.close()

#     return ids_actualizados_o_insertados  # Devuelve la lista de IDs procesados


# Eliminar una fila específica de la base de datos con ID dinámico
def eliminarFilaPorColumna(base, columna_id, valor_id):
    """
    Elimina una fila de la tabla especificada utilizando un identificador dinámico.

    Args:
        base (str): Nombre de la tabla de la base de datos.
        columna_id (str): Nombre de la columna que actúa como identificador.
        valor_id (int | str): Valor del identificador que se desea eliminar.

    Returns:
        bool: True si la fila fue eliminada, False si no se encontró.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

        # Habilitar las restricciones de claves foráneas (PRAGMA foreign_keys)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Generar la consulta SQL dinámicamente con el nombre de la columna
    query = f"DELETE FROM {base} WHERE {columna_id} = ?"
    cursor.execute(query, (valor_id,))
    conn.commit()
    rows_deleted = cursor.rowcount  # Número de filas afectadas

    conn.close()
    #carpeta=os.path.join(FINAL_UPLOAD_FOLDER, f"evento_{valor_id}")
    # try:
    #     for root, dirs, files in os.walk(carpeta, topdown=False):
    #         for file in files:
    #             os.remove(os.path.join(root, file))  # Eliminar archivo
    #         for dir in dirs:
    #             os.rmdir(os.path.join(root, dir))  # Eliminar subcarpeta vacía
    #     os.rmdir(carpeta)  # Eliminar la carpeta principal
    #     print(f"La carpeta '{carpeta}' ha sido eliminada.")
    # except FileNotFoundError:
    #     print(f"La carpeta '{carpeta}' no existe.")
    # except Exception as e:
    #     print(f"Error al eliminar la carpeta '{carpeta}': {e}")
    
    
    return rows_deleted > 0  # Retorna True si se eliminó algo, False si no



def cargarDatoID(base, columna_id, valor_id):
    """
    Carga los datos de una fila específica de una tabla en un diccionario dentro de la sesión.

    Args:
        base (str): Nombre de la tabla en la base de datos.
        columna_id (str): Nombre de la columna que actúa como identificador.
        valor_id (int | str): Valor del identificador de la fila que se quiere cargar.

    Returns:
        bool: True si los datos se cargaron correctamente en la sesión, False si no se encontró la fila.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener la información de la fila
    query = f"SELECT * FROM {base} WHERE {columna_id} = ?"
    cursor.execute(query, (valor_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False  # No se encontró la fila

    # Obtener los nombres de las columnas
    column_query = f"PRAGMA table_info({base})"
    cursor.execute(column_query)
    columns = [col[1] for col in cursor.fetchall()]  # Extraer nombres de columnas

    # Crear un diccionario con los datos de la fila
    session[base] = {columns[i]: row[i] for i in range(len(columns))}

    conn.close()
    return True  # Los datos se cargaron correctamente



def cargarDatosLista(base, campo, valor):
    """
    Carga todas las filas que coincidan con un valor específico en una columna en una variable de sesión.

    Args:
        base (str): Nombre de la tabla en la base de datos.
        campo (str): Nombre de la columna por la que se filtran los datos.
        valor (int | str): Valor que debe coincidir en la columna especificada.

    Returns:
        bool: True si se encontraron filas y se cargaron en la sesión, False si no hay coincidencias.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Consulta para obtener las filas que coincidan con el valor especificado
    query = f"SELECT * FROM {base} WHERE {campo} = ?"
    cursor.execute(query, (valor,))
    rows = cursor.fetchall()
    print("Rows:", rows)  # Verifica si se encontraron filas

    if not rows:
        conn.close()
        return False  # No se encontraron filas

    # Obtener los nombres de las columnas
    column_query = f"PRAGMA table_info({base})"
    cursor.execute(column_query)
    columns = [col[1] for col in cursor.fetchall()]  # Extraer nombres de columnas

    # Crear una lista de diccionarios con los datos de las filas encontradas
    session[base] = [
        {columns[i]: row[i] for i in range(len(columns))} for row in rows
    ]

    conn.close()
    return True  # Los datos se cargaron correctamente
