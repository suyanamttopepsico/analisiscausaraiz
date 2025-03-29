##############################################################################
#LIBRERÍAS
import streamlit as st
import os
import pandas as pd
##############################################################################          
#Diccionario de Tipo de Datos 
MapeoPM={
    0:'Emergencia',
    1:'Inspección y Monitoreo por Condición',
    2:'Preventivo',
    3:'Reparación',
    5:'Avería',
    7:'Limpieza',
    8:'Correctivo',
    9:'Trabajo Fuera de Inspección',
    10:'Caso de Garantía',
    11:'Caso de Seguro',
    13:'Auditoria y Seguridad Alimentaria',
    16:'Meeting',
    17:'Asistencia a Operaciones',
    18:'Legal',
    19:'Capacitación',
    22:'Medio Ambiente y Sustetabilidad',
    23:'Seguridad',
    27:'Modificación',
    29:'RCA',
    33:'Lubricación',
    34:'Calibración',
    35:'(IPS) Mejorar Perfec de Spec',
    37:' El trabajo generado por RCA'    
    }

ubicaciones_dict = {
    "PR": "Líneas de Producción",
    "BO": "Bodega",
    "SE": "Servicios",
    "ED": "Edificios",
    "PR-01": "PC-14",
    "PR-02": "PC-10",
    "PR-03": "Extruidos Suaves",
    "PR-04": "Extruidos Duros",
    "PR-05": "TC-1500",
    "PR-06": "Pellet",
    "PR-08": "Área de Obsoletos",
    "PR-09": "CCM1",
    "PR-10": "CCM2",
    "BO-01": "Almacén Producto Terminado APT",
    "BO-02": "Almacén Materia Prima",
    "BO-03": "Almacén de Materia Agrícola",
    "BO-04": "Almacén de Repuestos",
    "BO-05": "Bodega de Pifo",
    "SE-01": "Cuarto de Máquinas",
    "SE-02": "Almacenamiento de Utilities",
    "SE-03": "Subestación PTAR",
    "SE-04": "Planta de Almidón",
    "SE-05": "Sistema de Acondicionamiento de Aire",
    "ED-01": "Oficinas",
    "ED-02": "Depósitos",
    "ED-03": "Vigilancia",
    "ED-04": "Areas Deportivas",
    "ED-05": "Estacionamiento",
    "ED-06": "Patios, calles y exteriores",
    "ED-07": "Área de Servicios y Exteriores"
}

#Diccionario de Tipo de Datos 
Mapeotécnico={
    81027427:'MECANIC2',
    80869611:'ELECTRI3',
    40028452:'MECANIC1',
    80927849:'ELECTRI1',
    30152518:'ELECMEC1',
    40285094:'ELECTRO2',
    80994331:'ELECTRI2',
    40028702:'ELECTRO1'
    }

Mapeotécnico2={
    'MECANIC2':'Rubén Pazmiño',
    'ELECTRI3':'Javier Solano',
    'MECANIC1':'Patricio Chávez',
    'ELECTRI1':'Fernando Guapucal',
    'ELECMEC1':'Juan Morocho',
    'ELECTRO2':'Romel Tipan',
    'ELECTRI2':'Willian Pilaguano',
    'ELECTRO1':'Danilo Castellano',
    "OPEREMP2":"Alexis Aro"
    }
##############################################################################
def division_segura(x):
    # Verificar si el denominador es diferente de 0 antes de dividir
    if x['Cantidad Total'] != 0:
        return x['Trbjo real'] / x['Cantidad Total']
    else:
        return None 
##############################################################################   
def ruta():
    ruta = os.path.realpath(__file__)
    if os.path.isdir(ruta):
        return ruta
    else:
        return os.path.dirname(ruta)
##############################################################################    
def nombre_archivo(trans,fecha_inicio, fecha_fin):    
    fecha_inicio_texto=fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin_texto=fecha_fin.strftime('%Y-%m-%d')
    nombre_csv = f"{trans}_{fecha_inicio_texto}_{fecha_fin_texto}.txt"
    return nombre_csv
##############################################################################
def txtIW28(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("IW28",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=1)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df = df.replace("\t", ";", regex=True)
    dfFil=df.iloc[:, [0,1,2,3,4,5,6,7,8,9,12,21,22]]
    dfFil.columns = ['Aviso', 'Fecha',"Descripción", 'Orden', 'Equipo', 'Denominación de objeto técnico', 
                    'Ubicación técnica', 'CePl','Cl._x','Creado por','DurParada',"PtoTrbRes","Status del sistema"]
    # Convertir las columnas a tipo objeto
    dfFil['Aviso'] = dfFil['Aviso'].astype('Int64')
    dfFil['Orden'] = dfFil['Orden'].astype(object)
    dfFil['Equipo'] = dfFil['Equipo'].astype(object)
    dfFil['CePl'] = dfFil['CePl'].astype(object)
    
    # Convertir la columna 'Duración parada' a tipo float
    dfFil['DurParada'] = dfFil['DurParada'].astype(str)
    dfFil['DurParada'] = dfFil['DurParada'].str.replace(',', '')
    dfFil['DurParada'] = dfFil['DurParada'].astype(float)
    dfFil['Fecha de aviso'] = pd.to_datetime(dfFil['Fecha'],format='%d.%m.%Y', errors='coerce')
    # Ordenar el DataFrame por la columna de fecha de manera ascendente
    df_sorted = dfFil.sort_values(by='Fecha de aviso', ascending=True)

    return df_sorted
##############################################################################
def txtIW38(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("IW38",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=0)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    # Convertir la columna de fecha a formato datetime
    dfFil=df.iloc[:, [0,1,2,3,4,5,6,7,10,11,12,30,68,69,70,71]]
    dfFil.columns = ["CePl","Aviso",'Orden',"Texto breve", 'Inic.extr.', 
                   'Ubicación técnica', 'Equipo',"PtoTrbRes",
                   "Fin real","Status del sistema","SumCosReal","Cl.","AMa","GP",
                   "Posicion","Plan M"]
    
    dfFil['Fin real'] = pd.to_datetime(dfFil['Fin real'],format='%d.%m.%Y', errors='coerce')
    dfFil['Inic.extr.'] = pd.to_datetime(dfFil['Inic.extr.'],format='%d.%m.%Y', errors='coerce')
    dfFil['SumCosReal']=dfFil['SumCosReal'].str.replace('.', '').str.replace(',', '.').astype(float)
    dfFil['Orden']=dfFil['Orden'].astype(object)

    # Ordena el DataFrame por la columna de fecha de manera ascendente
    df_sorted = dfFil.sort_values(by='Inic.extr.', ascending=True)
    return df_sorted
##############################################################################
def txtIW47(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("IW47",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=1)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df = df.replace("\t", ";", regex=True)
    # Convertir las columnas a tipo objeto
    dfFil=df.iloc[:, [5,10,15,21,23,39,41,46]]
    dfFil.columns = ["Orden","Fe.contab.","Trbjo real","Fe.in.real",'FecFinReal',
                     "PtoTrReal","CePl","Ubicación técnica"]
    
    dfFil['FecFinReal'] = pd.to_datetime(dfFil['FecFinReal'],format='%d.%m.%Y', errors='coerce')
    dfFil['Fe.contab.'] = pd.to_datetime(dfFil['Fe.contab.'],format='%d.%m.%Y', errors='coerce')
    dfFil['Fe.in.real'] = pd.to_datetime(dfFil['Fe.in.real'],format='%d.%m.%Y', errors='coerce')
    dfFil["Trbjo real"] = dfFil['Trbjo real'].astype(str)
    dfFil["Trbjo real"] = dfFil['Trbjo real'].str.replace(',', '')
    dfFil['Trbjo real'] = dfFil['Trbjo real'].astype(float)
    
    # Ordenar el DataFrame por la columna de fecha de manera ascendente
    df_sorted = dfFil
    
    return df_sorted
##############################################################################
def txtIW69(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("IW69",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=1)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df = df.replace("\t", ";", regex=True)
    # Convertir las columnas a tipo objeto
    dfFil=df.iloc[:, [0,1,3,5,7,8,11,12,13,14,15,17,19,21,28,29,53,97]]
    dfFil.columns = ["Aviso","Descripción","Cl.","Denominación de objeto técnico","DurParada","Fecha",
                     "PtOb","Texto código parte objeto","GrCódPrb","CoAv","TextoGrpCód Problema",
                     "Caus","Texto código motivo","Cód.","P","Status del sistema","Denominación de la ubicación técnica","PtoTrbRes"]
    dfFil['Fecha de aviso'] = pd.to_datetime(dfFil['Fecha'],format='%d.%m.%Y', errors='coerce')

    # Ordena el DataFrame por la columna de fecha de manera ascendente
    df_sorted = dfFil.sort_values(by='Fecha de aviso', ascending=True)
    
    return df_sorted
##############################################################################
def txtIW65(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("IW65",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=1)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df = df.replace("\t", ";", regex=True)
    # Convertir las columnas a tipo objeto
    dfFil=df.iloc[:, [1,2,3,6,7,49,56,87]]
    dfFil.columns = ["Aviso","Grupo códigos","CdAc","CePl","Ubicac.técnica","Fecha","Orden","Hora.1"]
   
    dfFil['Fecha de aviso'] = pd.to_datetime(dfFil['Fecha'],format='%d.%m.%Y', errors='coerce')
    
    # Extraer horas, minutos y segundos sin usar pd.to_datetime
    dfFil['Aviso'] = dfFil['Aviso'].astype('Int64')
    dfFil['Hora.1'] = dfFil['Hora.1'].astype(str)
    dfFil[['Horas', 'Minutos', 'Segundos']] = dfFil['Hora.1'].str.split(':', expand=True)
    dfFil['Horas'] = pd.to_numeric(dfFil['Horas'], errors='coerce').fillna(0).astype(int)
    dfFil['Minutos'] = pd.to_numeric(dfFil['Minutos'], errors='coerce').fillna(0).astype(int)
    dfFil['Segundos'] = pd.to_numeric(dfFil['Segundos'], errors='coerce').fillna(0).astype(int)
    
    # Calcular la suma total en formato decimal (hora + minuto / 60 + segundo / 3600)
    dfFil['Hora_decimal'] = dfFil['Horas'] + dfFil['Minutos'] / 60 + dfFil['Segundos'] / 3600

    # Ordena el DataFrame por la columna de fecha de manera ascendente
    df_sorted = dfFil.sort_values(by='Fecha de aviso', ascending=True)
    
    
    return df_sorted
##############################################################################
def txtMB51(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("MB51",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=1)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df = df.replace("\t", ";", regex=True)
    #st.write(df.columns)
    # Convertir las columnas a tipo objeto
    dfFil=df.iloc[:, [0,1,2,3,4,5,10,12,25,28,35,43]]
    dfFil.columns = ["Centro","Clase de movimiento","Texto de clase-mov.","Material","Texto breve de material","Cantidad",
                     "Fe.contabilización","Fecha de entrada","Orden","Fecha de documento","Importe ML","Ce.coste"]
    
    
    dfFil['Centro']=dfFil['Centro'].astype(object)
    dfFil['Clase de movimiento']=dfFil['Clase de movimiento'].astype(object)
    dfFil['Texto de clase-mov.']=dfFil['Texto de clase-mov.'].astype(object)
    dfFil['Material']=dfFil['Material'].astype(object)
    dfFil['Cantidad']=dfFil['Cantidad'].astype(str)
    dfFil['Cantidad']=dfFil['Cantidad'].str.replace(',', '').astype(float)
    dfFil['Importe ML']=dfFil['Importe ML'].astype(str)
    dfFil['Importe ML']=dfFil['Importe ML'].str.replace(',', '').astype(float)
    dfFil['Fecha de documento'] = pd.to_datetime(dfFil['Fecha de documento'],format='%d.%m.%Y', errors='coerce')
    dfFil['Fe.contabilización'] = pd.to_datetime(dfFil['Fe.contabilización'],format='%d.%m.%Y', errors='coerce')
    dfFil['Fecha de entrada'] = pd.to_datetime(dfFil['Fecha de entrada'],format='%d.%m.%Y', errors='coerce')

    return dfFil
##############################################################################
def txtKSB1(fecha_inicio, fecha_fin):
    nombreTxt=nombre_archivo("KSB1",fecha_inicio, fecha_fin)
    rut=ruta()
    os.chdir(rut)
    df=pd.read_csv(nombreTxt, sep="\t", header=0)
    unnamed_columns = [col for col in df.columns if "Unnamed" in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df = df.replace("\t", ";", regex=True)
    #st.write(df.columns)
    #st.write(df)
    # Convertir las columnas a tipo objeto
    dfFil=df.iloc[:, [0,3,5,6,11,65,56,12]]
    dfFil.columns = ["Fe.contab.","Ce.coste","Documento compra","Cuenta","N. documento","Valor","Texto de pedido","Valor moneda"]
    
    
    dfFil['Ce.coste']=dfFil['Ce.coste'].astype(object)
    dfFil['Cuenta']=dfFil['Cuenta'].astype(object)
    dfFil['N. documento']=dfFil['N. documento'].astype(object)
    dfFil['Documento compra']=dfFil['Documento compra'].astype(object)
    dfFil['Valor']=dfFil['Valor'].astype(str)
    dfFil['Valor']=dfFil['Valor'].str.replace(',', '').astype(float)
    dfFil['Valor moneda']=dfFil['Valor moneda'].astype(str)
    dfFil['Valor moneda']=dfFil['Valor moneda'].str.replace(',', '').astype(float)
    dfFil['Fe.contab.'] = pd.to_datetime(dfFil['Fe.contab.'],format='%d.%m.%Y', errors='coerce')

    return dfFil
###############################################################################
def procesamiento(df47, df69, df28, df38, dfkr):
    
    # Mapeo de códigos a nombres técnicos
    dfkr['PtoTrReal'] = dfkr['GPID'].map(Mapeotécnico)
    dfkr['Nombre Técnico'] = dfkr['PtoTrReal'].map(Mapeotécnico2)
    
    # Procesamiento de datos en df47
    df47 = df47.merge(df38[['Orden', 'Cl.', 'AMa']], on='Orden', how='left')

    df47['NombrePM'] = df47['AMa'].map(MapeoPM)
    df47['CodUbi'] = df47['Ubicación técnica'].apply(lambda x: x[11:16] if isinstance(x, str) and len(x) >= 16 else (x[11:] if isinstance(x, str) else x))
    df47['NombreUbi'] = df47['CodUbi'].map(ubicaciones_dict)
    df47['Nombre Técnico'] = df47['PtoTrReal'].map(Mapeotécnico2)
    df47 = df47.drop(df47[(df47['PtoTrReal'] == "MECANIC2") & (df47['Fe.contab.'] < '01.06.2023')].index)
    df47 = df47.drop(df47[df47['Trbjo real'] == 0].index)
    df47_agrup = df47.groupby(['FecFinReal', 'PtoTrReal', 'Ubicación técnica'])['Trbjo real'].sum().reset_index()
    df47_agrup['CodUbi'] = df47_agrup['Ubicación técnica'].apply(lambda x: x[11:16] if len(x) >= 16 else x[11:])
    df47_agrup['NombreUbi'] = df47_agrup['CodUbi'].map(ubicaciones_dict)
    df47_agrup = df47_agrup.drop('CodUbi', axis=1)
    df_ut = pd.merge(dfkr, df47_agrup, left_on=['Fecha', 'PtoTrReal'], right_on=['FecFinReal', 'PtoTrReal'], suffixes=('_dfkr', '_df47_agrup'), how='outer', indicator=True)
    df_ut['Utilización Técnica'] = (df_ut.apply(division_segura, axis=1)) * 100
    df_ut['Nombre Técnico'] = df_ut['PtoTrReal'].map(Mapeotécnico2)
    df_ut = df_ut.drop_duplicates(['Fecha', 'Nombre Técnico', 'Trbjo real', 'Ubicación técnica'])
       
    # Procesamiento de datos en df69
    
    df69['CodUbi'] = df69['Denominación de la ubicación técnica'].apply(lambda x: x[11:16] if isinstance(x, str) and len(x) >= 16 else (x[11:] if isinstance(x, str) else x))
    df69['Nombre Técnico'] = df69['PtoTrbRes'].map(Mapeotécnico2)
    df69['NombreUbi'] = df69['CodUbi'].map(ubicaciones_dict)
    df69 = df69.drop(df69[(df69['PtoTrbRes'] == "MECANIC2") & (df69['Fecha de aviso'] < '01.06.2023')].index)
    
    # Procesamiento de datos en df38
    df38['CodUbi'] = df38['Ubicación técnica'].apply(lambda x: x[11:16] if isinstance(x, str) and len(x) >= 16 else (x[11:] if isinstance(x, str) else x))
    df38['Nombre Técnico'] = df38['PtoTrbRes'].map(Mapeotécnico2)
    df38['NombreUbi'] = df38['CodUbi'].map(ubicaciones_dict)
    df38['NombrePM'] = df38['AMa'].map(MapeoPM)
 
    # Procesamiento de datos en df28
    df28['Fecha'] = df28['Fecha'].str.replace('.', '-')
    df28['Fecha de aviso'] = pd.to_datetime(df28['Fecha'], format='%d-%m-%Y', errors='coerce')
    df28['CodUbi'] = df28['Ubicación técnica'].apply(lambda x: x[11:16] if isinstance(x, str) and len(x) >= 16 else (x[11:] if isinstance(x, str) else x))
    df28['Nombre Técnico'] = df28['PtoTrbRes'].map(Mapeotécnico2)
    df28['NombreUbi'] = df28['CodUbi'].map(ubicaciones_dict)
    df28 = df28.merge(df38[['Orden', 'Cl.', 'AMa', 'NombrePM']], on='Orden', how='left')
    df28 = df28.drop(df28[(df28['PtoTrbRes'] == "MECANIC2") & (df28['Fecha de aviso'] < '2023-06-01')].index)
   
    # Calcula las fechas de inicio y fin para análisis
    fechainicio = max(
        pd.to_datetime(df38['Inic.extr.'], format='%d.%m.%Y', errors='coerce').min(),
        pd.to_datetime(df69['Fecha de aviso'], format='%d.%m.%Y', errors='coerce').min(),
        pd.to_datetime(df47['Fe.contab.'], format='%d.%m.%Y', errors='coerce').min()
    )
    fechafin = min(
        pd.to_datetime(df38['Inic.extr.'], format='%d.%m.%Y', errors='coerce').max(),
        pd.to_datetime(df69['Fecha de aviso'], format='%d.%m.%Y', errors='coerce').max(),
        pd.to_datetime(df47['Fe.contab.'], format='%d.%m.%Y', errors='coerce').max(),
        pd.to_datetime(dfkr['Fecha'], format='%d.%m.%Y', errors='coerce').max()
    )
    
    # Crea columnas en la interfaz
    col1, col2, col3 = st.columns([1, 1, 2])
    
    # Selecciona el período de análisis
    datestart, dateend = st.date_input("PERIÓDO DE ANÁLISIS", value=(fechainicio, fechafin), min_value=fechainicio, max_value=fechafin)
    date1inicio = pd.to_datetime(datestart)
    date2fin = pd.to_datetime(dateend)
    
    # Selecciona la ubicación
    linea = st.multiselect("UBICACIÓN", ubicaciones_dict.values(), placeholder="Seleccione una ubicación")
    
    # Selecciona el técnico de mantenimiento
    tecnico = st.selectbox("TÉCNICO", Mapeotécnico2.values(), index=None, placeholder="Seleccione un Técnico de Mantenimiento")

    #Manejo de dataframes según condiciones
    if linea and tecnico is None:
        # Realizar acciones cuando solo se ha seleccionado "UBICACIÓN" y no "TÉCNICO"
        df_47_graph = df47[(df47['FecFinReal'] >= date1inicio) & (df47['FecFinReal'] <= date2fin) & (df47['NombreUbi'].isin(linea))].copy()
        df_ut_dia = df_ut[(df_ut['FecFinReal'] >= date1inicio) & (df_ut['FecFinReal'] <= date2fin) & (df_ut['NombreUbi'].isin(linea))].copy()
        df_kr_graph=dfkr[(dfkr['Fecha']>=date1inicio)&(dfkr['Fecha']<=date2fin)].copy()
        df_28_graph=df28[(df28['Fecha de aviso'] >= date1inicio) & (df28['Fecha de aviso'] <= date2fin) & (df28['NombreUbi'].isin(linea))].copy()
        df_38_graph=df38[(df38['Inic.extr.'] >= date1inicio) & (df38['Inic.extr.'] <= date2fin) & (df38['NombreUbi'].isin(linea))].copy()
        df_69_graph=df69[(df69['Fecha de aviso'] >= date1inicio) & (df69['Fecha de aviso'] <= date2fin) & (df69['NombreUbi'].isin(linea))].copy()
    elif not linea  and tecnico:
        # Realizar acciones cuando solo se ha seleccionado "TÉCNICO" y no "UBICACIÓN"
        df_47_graph = df47[(df47['FecFinReal'] >= date1inicio) & (df47['FecFinReal'] <= date2fin) & (df47['Nombre Técnico'] == tecnico)].copy()
        df_ut_dia = df_ut[(df_ut['FecFinReal'] >= date1inicio) & (df_ut['FecFinReal'] <= date2fin) & (df_ut['Nombre Técnico'] == tecnico)].copy()
        df_kr_graph=dfkr[(dfkr['Fecha']>=date1inicio)&(dfkr['Fecha']<=date2fin) & (dfkr['Nombre Técnico'] == tecnico)].copy()
        df_28_graph=df28[(df28['Fecha de aviso'] >= date1inicio) & (df28['Fecha de aviso'] <= date2fin) & (df28['Nombre Técnico'] == tecnico)].copy()
        df_38_graph=df38[(df38['Inic.extr.'] >= date1inicio) & (df38['Inic.extr.'] <= date2fin) & (df38['Nombre Técnico'] == tecnico)].copy()
        df_69_graph=df69[(df69['Fecha de aviso'] >= date1inicio) & (df69['Fecha de aviso'] <= date2fin) & (df69['Nombre Técnico'] == tecnico)].copy()
    elif linea and tecnico:
        # Realizar acciones cuando se han seleccionado tanto "UBICACIÓN" como "TÉCNICO" o ninguno
        df_47_graph = df47[(df47['FecFinReal'] >= date1inicio) & (df47['FecFinReal'] <= date2fin) & (df47['Nombre Técnico'] == tecnico)&(df47['NombreUbi'].isin(linea))].copy()
        df_ut_dia = df_ut[(df_ut['FecFinReal'] >= date1inicio) & (df_ut['FecFinReal'] <= date2fin) & (df_ut['Nombre Técnico'] == tecnico)&(df_ut['NombreUbi'].isin(linea))].copy()
        df_28_graph=df28[(df28['Fecha de aviso'] >= date1inicio) & (df28['Fecha de aviso'] <= date2fin) & (df28['Nombre Técnico'] == tecnico)&(df28['NombreUbi'].isin(linea))].copy()
        df_38_graph=df38[(df38['Inic.extr.'] >= date1inicio) & (df38['Inic.extr.'] <= date2fin) & (df38['NombreUbi'].isin(linea))&(df38['Nombre Técnico'] == tecnico)].copy()
        df_69_graph=df69[(df69['Fecha de aviso'] >= date1inicio) & (df69['Fecha de aviso'] <= date2fin) & (df69['Nombre Técnico'] == tecnico)&(df69['NombreUbi'].isin(linea))].copy()
        df_kr_graph=dfkr[(dfkr['Fecha']>=date1inicio)&(dfkr['Fecha']<=date2fin) & (dfkr['Nombre Técnico'] == tecnico)].copy()
    else:
        # Realizar acciones cuando se han seleccionado tanto "UBICACIÓN" como "TÉCNICO" o ninguno
        df_47_graph = df47[(df47['FecFinReal'] >= date1inicio) & (df47['FecFinReal'] <= date2fin)].copy()
        df_ut_dia = df_ut[(df_ut['FecFinReal'] >= date1inicio) & (df_ut['FecFinReal'] <= date2fin)].copy()
        df_kr_graph=dfkr[(dfkr['Fecha']>=date1inicio)&(dfkr['Fecha']<=date2fin)].copy()
        df_28_graph=df28[(df28['Fecha de aviso'] >= date1inicio) & (df28['Fecha de aviso'] <= date2fin)].copy()
        df_38_graph=df38[(df38['Inic.extr.'] >= date1inicio) & (df38['Inic.extr.'] <= date2fin)].copy()
        df_69_graph=df69[(df69['Fecha de aviso'] >= date1inicio) & (df69['Fecha de aviso'] <= date2fin)].copy()
    return df_47_graph, df_ut_dia, df_kr_graph, df_28_graph, df_38_graph, df_69_graph





