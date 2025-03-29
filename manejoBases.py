from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import pandas as pd
import os



bases={
    "evento":["ID", "Categoria", "Fecha Evento", "OT Avería", "OT RCA", "Planta", 
            "Línea Producción", "Área Empresa", "Cod SAP", "Nombre Equipo SAP",
            "Causa RCA", "Costos", "Tiempo Total","MTBF","MTTR", "Técnico", 
            "Representante Mantenimiento", "Representante SASS", "Representante Calidad", 
            "Representante Producción","Terminado","Aprobado","Aprobado Regional","Aproador Local","Autor"],
    "equipo":["Nombre","Imagen","Fabricante","Detalles técnicos","Evento","Autor"],
    "secuencia":["Índice","Nombre","Evento","Autor"],
    "condiciones":["Índice","Descripción","Imagen","Secuencia","Evento","Autor"],
    "problema":["Componente","Parte de Componente","Difiere estado normal",
                 "Problema repetitivo","Problema previo","Detalles Problema repetitivo","Detalles Problema Previo","Imagen de Avería","Autor","Evento"],
    "fenomeno":["Que","Cuando","Donde","Quien","Cual","Como","OPL","Detalles de los hechos","Evento","Autor"],
    "cincoporque":["Primer porque","Primera respuesta","Segundo porque","Segunda respuesta","Tercer porque",
                   "Tercera respuesta","Cuarto porque","Cuarta respuesta","Quinto porque","Quinta respuesta","Tipo de averia","Evento","Autor"],
    "contramedidas":["Índice","Tipo","Descripción breve","OT SAP","Fecha de cumplimiento",'OT Completado',"Evento","Autor"],
    "usuarios":['ID_user','username', 'password', 'email', 'first_name', 'last_name', 'position', 'country', 'plant', 'phone', 'sap_position']  
}


###############################################################################
ruta=os.path.join(os.getcwd(), "base")
###############################################################################
# Función para leer o crear la base de datos
def lecturaBase(base):

    nombreBase=os.path.join(ruta, f"{base}.txt")

    if os.path.exists(nombreBase):
        df = pd.read_csv(nombreBase, sep="\t") 
    else:
        # Crear DataFrame vacío con columnas definidas
        df = pd.DataFrame(columns=bases[base])

    return df,nombreBase

###############################################################################
# Función para agregar una fila a la base de datos
def agregarFilaID(data,base):
    [df,nombreBase] = lecturaBase(base)

    # Asignar el ID a la nueva fila
    if len(df) == 0:
        ID = 1
    else:
        ID = df["ID"].max() + 1  
    
    # Añadir el número al diccionario de datos
    data['ID'] = ID
    
    # Concatenar los datos nuevos con los existentes
    aux = pd.DataFrame([data])
    dfR = pd.concat([df, aux], ignore_index=False)
    
    # Guardar el DataFrame actualizado
    dfR.to_csv(nombreBase, sep="\t", index=False)
    return ID

def agregarFila(data,base,campo,campoValor):
    [df,nombreBase] = lecturaBase(base)
    # Concatenar los datos nuevos con los existentes
    aux = pd.DataFrame(data)
    aux[campo]=campoValor

    dfR = pd.concat([df, aux], ignore_index=False)
    
    # Guardar el DataFrame actualizado
    dfR.to_csv(nombreBase, sep="\t", index=False)
###############################################################################
###############################################################################