# -*- coding: utf-8 -*-
"""
Lectura desde SAP

@author: 81136187
"""
##############################################################################
#LIBRERÍAS
import os

import webbrowser
import win32com.client
import time
from datetime import datetime
import sys
import pandas as pd
##############################################################################
def barraProgreso(paso_actual, total_pasos, prefix="", size=100):
    percent = paso_actual / total_pasos
    bar = "#" * int(size * percent)
    sys.stdout.write(f"\r{prefix} [{bar:<{size}}] {percent*100:.1f}%")
    sys.stdout.flush()
##############################################################################
def navegador():
    """
    Abre el navegador y carga la URL especificada.
    """
    SapGuiAuto = None
    url = "https://sapp33.mypepsico.com/irj/portal"
    webbrowser.open(url)
    
    # Esperar hasta que se abra SAP GUI
    while SapGuiAuto is None:
        try:
            SapGuiAuto = win32com.client.GetObject("SAPGUI")
        except Exception as e:
            SapGuiAuto = None
        time.sleep(1)
##############################################################################
def conexionSAP():
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")   
    except Exception as e:
        print("SAP no está abierto. Se iniciará el navegador.")
        SapGuiAuto = None
        navegador()
        session=conexionSAP()       
    time.sleep(1)            
    if SapGuiAuto is not None:
        Application = SapGuiAuto.GetScriptingEngine
        Connection = Application.Children(0)
        session = Connection.Children(0)
    return session  
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
def Sap2TXT(trans, rows, session, fecha_inicio, fecha_fin):
    rut=f"{ruta()}"
    rut=os.path.join(rut, 'base', 'SAPINFO')
    nombreTxt=nombre_archivo(trans,fecha_inicio, fecha_fin)
    session.findById("wnd[0]/mbar/menu[5]/menu[2]/menu[0]").select()
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/cntlCONTAINER1_LAYO/shellcont/shell").selectedRows = rows
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/btnAPP_WL_SING").press()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/mbar/menu[0]/menu[11]/menu[2]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = nombreTxt
    session.findById("wnd[1]/usr/ctxtDY_PATH").text = rut
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/okcd").text = "/NMEN"
    session.findById("wnd[0]").sendVKey(0)
##############################################################################
def MB2TXT(trans, rows, session, fecha_inicio, fecha_fin):
    rut=f"{ruta()}"
    nombreTxt=nombre_archivo(trans,fecha_inicio, fecha_fin)
    session.findById("wnd[0]/mbar/menu[3]/menu[2]/menu[0]").select()
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/cntlCONTAINER1_LAYO/shellcont/shell").selectedRows = rows
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/btnAPP_WL_SING").press()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/mbar/menu[0]/menu[1]/menu[2]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = nombreTxt
    session.findById("wnd[1]/usr/ctxtDY_PATH").text = rut
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/okcd").text = "/NMEN"
    session.findById("wnd[0]").sendVKey(0)
##############################################################################    
def sapIW28(session, fecha_inicio, fecha_fin, planta):
    
    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="IW28", size=100)
    # Establece el código de transacción en IW28
    session.findById("wnd[0]/tbar[0]/okcd").text = "IW28"
    session.findById("wnd[0]").sendVKey(0)

    # Selecciona las casillas de verificación
    session.findById("wnd[0]/usr/chkDY_RST").selected = True
    session.findById("wnd[0]/usr/chkDY_MAB").selected = True

    # Establece los valores de filtro
    session.findById("wnd[0]/usr/ctxtQMART-LOW").text = "Z1"
    session.findById("wnd[0]/usr/ctxtQMART-HIGH").text = "Z3"
    session.findById("wnd[0]/usr/ctxtDATUV").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtDATUB").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/btn%_SWERK_%_APP_%-VALU_PUSH").press()
    for i in range(len(planta)):
        session.findById(f"wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,{i}]").text = planta[i]
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").setFocus
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").caretPosition = 4
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/usr/ctxtVARIANT").setFocus
    session.findById("wnd[0]/usr/ctxtVARIANT").caretPosition = 6
    session.findById("wnd[0]").sendVKey(8)
    
    #Creación de archivo de texto
    barraProgreso(paso+50, total_pasos, prefix="IW28", size=100)
    Sap2TXT("IW28","0-86", session, fecha_inicio, fecha_fin)
    barraProgreso(paso+100, total_pasos, prefix="IW28", size=100)
##############################################################################
def sapIW38(session, fecha_inicio, fecha_fin, planta):
    
    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="IW38", size=100)
    # Establece el código de transacción en IW38
    session.findById("wnd[0]/tbar[0]/okcd").text = "IW38"
    session.findById("wnd[0]").sendVKey(0)
    
    # Selecciona las casillas de verificación
    session.findById("wnd[0]/usr/chkDY_MAB").selected = True
    session.findById("wnd[0]/usr/chkDY_HIS").selected = True
    
    # Establece los valores de filtro
    session.findById("wnd[0]/usr/ctxtAUART-LOW").text = "ZB01"
    session.findById("wnd[0]/usr/ctxtAUART-HIGH").text = "ZB05"
    session.findById("wnd[0]/usr/ctxtDATUV").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtDATUB").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/btn%_SWERK_%_APP_%-VALU_PUSH").press()
    for i in range(len(planta)):
        session.findById(f"wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,{i}]").text = planta[i]
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").setFocus
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").caretPosition = 4
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/usr/ctxtIWERK-LOW").setFocus
    session.findById("wnd[0]/usr/ctxtIWERK-LOW").caretPosition = 4
    session.findById("wnd[0]").sendVKey(8)
    
    #Creación de archivo de texto
    session.findById("wnd[0]/mbar/menu[5]/menu[2]/menu[0]").select()
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/cntlCONTAINER1_LAYO/shellcont/shell").selectedRows = "0-56"
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/btnAPP_WL_SING").press()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    barraProgreso(paso+50, total_pasos, prefix="IW38", size=100)
    Sap2TXT("IW38","54-55",session, fecha_inicio, fecha_fin)
    barraProgreso(paso+100, total_pasos, prefix="IW38", size=100)
##############################################################################
def sapIW69(session, fecha_inicio, fecha_fin):
    
    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="IW69", size=100)
    # Establece el código de transacción en IW69
    session.findById("wnd[0]/tbar[0]/okcd").text = "IW69"
    session.findById("wnd[0]").sendVKey(0)

    # Establece los valores de filtro
    session.findById("wnd[0]/usr/ctxtDATUV").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtDATUB").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtIWERK-LOW").text = "8600"
    session.findById("wnd[0]/usr/ctxtIWERK-LOW").setFocus
    session.findById("wnd[0]/usr/ctxtIWERK-LOW").caretPosition = 4
    session.findById("wnd[0]").sendVKey(8)
    
    #Creación de archivo de texto
    barraProgreso(paso+50, total_pasos, prefix="IW69", size=100)
    Sap2TXT("IW69","0-86",session, fecha_inicio, fecha_fin)
    barraProgreso(paso+100, total_pasos, prefix="IW69", size=100)
##############################################################################
def sapIW65(session, fecha_inicio, fecha_fin, planta):
    
    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="IW65", size=100)
    
    # Establece el código de transacción en IW65
    session.findById("wnd[0]/tbar[0]/okcd").text = "IW65"
    session.findById("wnd[0]").sendVKey(0)
    
    #Establecer filtro
    session.findById("wnd[0]/usr/ctxtQMART-LOW").text = "Z5"
    session.findById("wnd[0]/usr/ctxtDATUV").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtDATUB").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/btn%_SWERK_%_APP_%-VALU_PUSH").press()
    for i in range(len(planta)):
        session.findById(f"wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,{i}]").text = planta[i]
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").setFocus
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").caretPosition = 4
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/tbar[1]/btn[8]").press()
    
    #Creación de archivo de texto
    barraProgreso(paso+50, total_pasos, prefix="IW65", size=100)
    Sap2TXT("IW65","0-123",session, fecha_inicio, fecha_fin)
    barraProgreso(paso+100, total_pasos, prefix="IW65", size=100)
    
##############################################################################
def sapIW47(session, fecha_inicio, fecha_fin,planta):

    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="IW47", size=100)
    # Establece el código de transacción en IW69
    session.findById("wnd[0]/tbar[0]/okcd").text = "IW47"
    session.findById("wnd[0]").sendVKey(0)
    
    # Selecciona las casillas de verificación
    session.findById("wnd[0]/usr/chkDY_IAR").selected = True
    session.findById("wnd[0]/usr/chkDY_ABG").selected = True
    
    # Establece los valores de filtro
    session.findById("wnd[0]/usr/btn%_WERKS_O_%_APP_%-VALU_PUSH").press()
    for i in range(len(planta)):
        session.findById(f"wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,{i}]").text = planta[i]
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").setFocus
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").caretPosition = 4
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/usr/ctxtERSDA_C-LOW").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtERSDA_C-HIGH").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtERSDA_C-LOW").setFocus
    session.findById("wnd[0]/usr/ctxtERSDA_C-LOW").caretPosition = 10
    session.findById("wnd[0]").sendVKey(8)
    
    #Creación de archivo de texto
    barraProgreso(paso+50, total_pasos, prefix="IW47", size=100)
    Sap2TXT("IW47","0-53",session, fecha_inicio, fecha_fin)
    barraProgreso(paso+100, total_pasos, prefix="", size=100)
###############################################################################
def sapMB51(session, fecha_inicio, fecha_fin):
    
    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="MB51", size=100)
    
    # Establece el código de transacción en MB51
    session.findById("wnd[0]/tbar[0]/okcd").text = "MB51"
    session.findById("wnd[0]").sendVKey(0)
    
    # Establece los valores de filtro
    planta=["8600","8500","8700","8780"]
    planta = pd.DataFrame(planta)
    planta.to_clipboard(index=False)
    session.findById("wnd[0]/usr/btn%_WERKS_%_APP_%-VALU_PUSH").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/usr/ctxtLGORT-LOW").text = "RF01"
    session.findById("wnd[0]/usr/ctxtBWART-LOW").text = "201"
    session.findById("wnd[0]/usr/ctxtBWART-HIGH").text = "262"
    session.findById("wnd[0]/usr/ctxtBUDAT-LOW").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtBUDAT-HIGH").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/tbar[1]/btn[8]").press()
    
    #Creación de archivo de texto
    barraProgreso(paso+50, total_pasos, prefix="MB51", size=100)
    MB2TXT("MB51","0-51",session, fecha_inicio, fecha_fin)
    barraProgreso(paso+100, total_pasos, prefix="MB51", size=100)

##############################################################################
def sapKSB1(session, fecha_inicio, fecha_fin):
    
    total_pasos = 100
    paso=0
    barraProgreso(paso, total_pasos, prefix="KSB1", size=100)
    
    #Ingreso a transacción
    session.findById("wnd[0]/tbar[0]/okcd").text = "KSB1"
    session.findById("wnd[0]").sendVKey(0)
    #Selección de bloque de análisis (Pepsico Internacional)
    session.findById("wnd[0]/usr/ctxtP_KOKRS").text = "PI01"
    #Ingreso de centros de costo a analizar
    session.findById("wnd[0]/usr/btn%_KOSTL_%_APP_%-VALU_PUSH").press()
    centros=["EC11006","EC11004","EC11009","EC11008",
             "CO11714","CO11715","CO11727",
             "CO11714","CO11715","CO11727",
             "PE11104","PE11101","PE11107","PE11106"]
    centros = pd.DataFrame(centros)
    centros.to_clipboard(index=False)
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    #Ingreso de cuentas a analizar
    session.findById("wnd[0]/usr/btn%_KSTAR_%_APP_%-VALU_PUSH").press()
    cuentas=["6300081","6000100","6000110","6300080","6300082","6100500","6100110","6100112","6100300","6100600","6100601","6000200","6000215","6000511","6100610"]
    cuentas = pd.DataFrame(cuentas)
    cuentas.to_clipboard(index=False)
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    #Ingreso de fecha de análisis
    session.findById("wnd[0]/usr/ctxtR_BUDAT-LOW").text = fecha_inicio.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtR_BUDAT-HIGH").text = fecha_fin.strftime("%d.%m.%Y")
    session.findById("wnd[0]/usr/ctxtR_BUDAT-HIGH").setFocus
    session.findById("wnd[0]/usr/ctxtR_BUDAT-HIGH").caretPosition = 10
    session.findById("wnd[0]/tbar[1]/btn[8]").press()
    #Definición de "layout"
    barraProgreso(paso+50, total_pasos, prefix="KSB1", size=100)
    session.findById("wnd[0]/mbar/menu[3]/menu[0]/menu[0]").select()
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/cntlCONTAINER1_LAYO/shellcont/shell").selectedRows = "0-42"
    session.findById("wnd[1]/usr/tabsG_TS_ALV/tabpALV_M_R1/ssubSUB_DYN0510:SAPLSKBH:0620/btnAPP_WL_SING").press()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    #Conversión a archivo plano
    session.findById("wnd[0]/mbar/menu[0]/menu[3]/menu[2]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[1]/usr/ctxtDY_PATH").setFocus
    session.findById("wnd[1]/usr/ctxtDY_PATH").caretPosition = 0
    session.findById("wnd[1]").sendVKey(4)
    rut=f"{ruta()}"
    nombreTxt=nombre_archivo("KSB1",fecha_inicio, fecha_fin)
    session.findById("wnd[2]/usr/ctxtDY_PATH").text = rut
    session.findById("wnd[2]/usr/ctxtDY_FILENAME").text = nombreTxt
    session.findById("wnd[2]/tbar[0]/btn[0]").press()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/okcd").text = "/NMEN"
    session.findById("wnd[0]").sendVKey(0)
    
    #Limpieza de caracteres extraños
    with open(nombreTxt, 'r',encoding='utf-8') as f:
        contenido = f.read()
    contenidoM = contenido.replace('"', '')
    with open(nombreTxt, 'w',encoding='utf-8') as f:
        f.write(contenidoM)
        
      
    barraProgreso(paso+100, total_pasos, prefix="KSB1", size=100)
##############################################################################
def lecturaSAPandinos(fecha_inicio, fecha_fin,codplanta):
    session=conexionSAP()
    fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d')
    planta=[codplanta]
    sapIW47(session, fecha_inicio, fecha_fin,planta)
    sapIW65(session, fecha_inicio, fecha_fin,planta)
    sapIW28(session, fecha_inicio, fecha_fin,planta)
    sapIW38(session, fecha_inicio, fecha_fin, planta)
    

