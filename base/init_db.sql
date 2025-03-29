-- Tabla de eventos
CREATE TABLE evento (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Categoria TEXT,
    Fecha_Evento DATE,
    OT_Averia TEXT,
    OT_RCA TEXT,
    Planta TEXT,
    Linea_Produccion TEXT,
    Area_Empresa TEXT,
    Cod_SAP TEXT,
    Nombre_Equipo_SAP TEXT,
    Causa_RCA TEXT,
    Costos REAL,
    Tiempo_Total REAL,
    MTBF REAL,
    MTTR REAL,
    Tecnico TEXT,
    Representante_Mantenimiento TEXT,
    Representante_SASS TEXT,
    Representante_Calidad TEXT,
    Representante_Produccion TEXT,
    Terminado BOOLEAN,
    Aprobado BOOLEAN,
    Aprobado_Regional TEXT,
    Aproador_Local TEXT,
    Autor TEXT
);

-- Tabla de equipos
CREATE TABLE equipo (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT,
    Imagen TEXT,
    Fabricante TEXT,
    Detalles_Tecnicos TEXT,
    Evento INTEGER,
    Autor TEXT,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de secuencias
CREATE TABLE secuencia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Indice INTEGER,
    Nombre TEXT,
    Evento INTEGER,
    Autor TEXT,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de condiciones
CREATE TABLE condiciones (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Indice INTEGER,
    Descripcion TEXT,
    Imagen TEXT,
    Secuencia INTEGER,
    Evento INTEGER,
    Autor TEXT,
    FOREIGN KEY (Secuencia) REFERENCES secuencia(ID) ON DELETE CASCADE,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de problemas
CREATE TABLE problema (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Componente TEXT,
    Parte_de_Componente TEXT,
    Difiere_estado_normal TEXT,
    Problema_repetitivo BOOLEAN,
    Problema_previo BOOLEAN,
    Detalles_Problema_repetitivo TEXT,
    Detalles_Problema_Previo TEXT,
    Imagen_de_Averia TEXT,
    Autor TEXT,
    Evento INTEGER,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de fenómenos
CREATE TABLE fenomeno (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Que TEXT,
    Cuando TEXT,
    Donde TEXT,
    Quien TEXT,
    Cual TEXT,
    Como TEXT,
    OPL TEXT,
    Detalles_de_los_hechos TEXT,
    Evento INTEGER,
    Autor TEXT,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de 5 porqués
CREATE TABLE cincoporque (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Primer_porque TEXT,
    Primera_respuesta TEXT,
    Segundo_porque TEXT,
    Segunda_respuesta TEXT,
    Tercer_porque TEXT,
    Tercera_respuesta TEXT,
    Cuarto_porque TEXT,
    Cuarta_respuesta TEXT,
    Quinto_porque TEXT,
    Quinta_respuesta TEXT,
    Tipo_de_averia TEXT,
    Evento INTEGER,
    Autor TEXT,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de contramedidas
CREATE TABLE contramedidas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Indice INTEGER,
    Tipo TEXT,
    Descripcion_breve TEXT,
    OT_SAP TEXT,
    Fecha_de_cumplimiento DATE,
    OT_Completado BOOLEAN,
    Evento INTEGER,
    Autor TEXT,
    FOREIGN KEY (Evento) REFERENCES evento(ID) ON DELETE CASCADE
);

-- Tabla de usuarios
CREATE TABLE usuarios (
    ID_user INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    position TEXT,
    country TEXT,
    plant TEXT,
    phone TEXT,
    sap_position TEXT,
    pending_approval BOOLEAN
);
