from flask import Flask, send_file
from reportlab.lib.pagesizes import A4, inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,Image,HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import CondPageBreak
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os 
from reportlab.platypus import Paragraph, Spacer, HRFlowable

def is_valid(value):
    return value not in [None, "None", "", "null"]

def add_section_divider(story, title):
    styles = getSampleStyleSheet()
    
    # Estilo del texto del título
    section_title_style = ParagraphStyle(
        "CustomTitleStyle",
        parent=styles["Heading5"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.white,
        alignment=1,  # 1 = Alineación centrada
    )

    # Texto dentro de la celda
    section_title = Paragraph(title, section_title_style)

    # Crear una tabla para darle fondo al texto
    table_data = [[section_title]]  
    table = Table(table_data, colWidths="100%")  # Ancho total

    # Aplicar estilos a la tabla (fondo azul PepsiCo)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#004B93")),  # Fondo azul
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),  # Texto blanco
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Texto centrado
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Alineación vertical
        ("PADDING", (0, 0), (-1, -1), 6),  # Espaciado interno
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Espaciado inferior pequeño
    ]))

    # Agregar espacio antes y después para separación
    story.append(Spacer(1, 10))
    story.append(table)
    story.append(Spacer(1, 10))

def add_sub_section_divider(story, title):
    styles = getSampleStyleSheet()
    
    # Estilo del texto del título
    section_title_style = ParagraphStyle(
        "CustomTitleStyle",
        parent=styles["Heading5"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=colors.black,
        alignment=0,  # 1 = Alineación centrada
    )

    # Texto dentro de la celda
    section_title = Paragraph(title, section_title_style)

    # Crear una tabla para darle fondo al texto
    table_data = [[section_title]]  
    table = Table(table_data, colWidths="100%")  # Ancho total

    # Aplicar estilos a la tabla (fondo azul PepsiCo)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#99BADD")),  # Fondo azul
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),  # Texto blanco
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Texto centrado
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Alineación vertical
        ("PADDING", (0, 0), (-1, -1), 6),# Espaciado interno
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Espaciado inferior pequeño
    ]))

    # Agregar espacio antes y después para separación
    story.append(Spacer(1, 10))
    story.append(table)
    story.append(Spacer(1, 10))



app = Flask(__name__)

def header_footer(canvas, doc, data):
    # Header
    header_text = f"Mantenimiento Andinos: Planta {data['evento']['Planta']}"
    canvas.setFont("Helvetica-Bold", 9)

    # Tamaños y posiciones
    left_image_path = "static/images/LogoPepsico.png"  # Imagen a la izquierda
    if data['evento']['Planta']=="Suyana":
        right_image_path = "static/images/Ecuador.png"  # Imagen a la derecha
    elif data['evento']['Planta']=="Funza" or data['evento']['Planta']=="Oriente":
        right_image_path = "static/images/Colombia.png"  # Imagen a la derecha
    elif data['evento']['Planta']=="Santa Anita":
        right_image_path = "static/images/Peru.png"  # Imagen a la derecha
    elif data['evento']['Planta']=="Santa Cruz":
        right_image_path = "static/images/Venezuela.png"  # Imagen a la derecha
    else:
        right_image_path = "static/images/LogoPepsico.png"  # Imagen a la derecha     
    left_image_x = 30  # Posición en X de la imagen izquierda
    left_image_y = doc.pagesize[1] - 50  # Posición en Y (arriba del todo)
    right_image_x = doc.pagesize[0] * 0.55  # Justo después del texto
    right_image_y = doc.pagesize[1] - 40  # Misma altura que la izquierda
    image_width, image_height = 120, 50  # Tamaño de las imágenes
    image_width_right, image_height_right = 50, 30  # Tamaño de las imágenes

    # Dibujar imágenes
    canvas.drawImage(left_image_path, left_image_x, left_image_y, width=image_width, height=image_height, preserveAspectRatio=True, mask='auto')
    canvas.drawImage(right_image_path, right_image_x, right_image_y, width=image_width_right, height=image_height_right, preserveAspectRatio=True, mask='auto')

    # Dibujar el texto del header
    text_x = doc.pagesize[0] * 0.65
    text_y = doc.pagesize[1] - 30
    canvas.drawString(text_x, text_y, header_text)

    # Footer con número de página
    canvas.setFont("Helvetica", 10)
    page_number = f"Página {doc.page}"
    canvas.drawString(doc.pagesize[0] - 100, 30, page_number)


def generate_pdf(data, output_filename):
    buffer = BytesIO()  # Use BytesIO to store the PDF in memory
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Create the story directly in the document
    story = Story(data)  # Create a Story instance
    #doc.build(story.elements, onFirstPage=header_footer, onLaterPages=header_footer)
    doc.build(story.elements, onFirstPage=lambda canvas, doc: header_footer(canvas, doc, data), onLaterPages=lambda canvas, doc: header_footer(canvas, doc, data))
    
    buffer.seek(0)  # Move back to the beginning of the BytesIO buffer
    return buffer

class Story:
    def __init__(self, data):
        self.elements = []  # This is where the elements will be stored
        self.styles = getSampleStyleSheet()
        self.data = data
        self.create_story()

    def create_story(self):
        # Header
        # header_text = f"<b>Mantenimiento Andinos</b>: Planta {self.data['evento']['Planta']}"
        # self.elements.append(Spacer(1, 12))
        # self.elements.append(Paragraph(header_text, self.styles['Normal']))

        # Title
        title = "INFORME DE ANÁLISIS CAUSA RAÍZ"
        self.elements.append(CondPageBreak(10))
        self.elements.append(Spacer(5, 0))
        self.elements.append(Paragraph(title, self.styles['Title']))
        first_col_style = ParagraphStyle(
            'FirstColStyle',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            )

        # Body content with event description
        body_text = f"""Este documento es un informe generado a partir del RCA realizado por 
                        <b>{self.data['evento']['Autor']}</b>"""
        if self.data['evento']['Autor'] == self.data['evento']['Tecnico']:
            body_text += f", técnico de mantenimiento de la planta {self.data['evento']['Planta']}."
        else:
            body_text += f" en conjunto con el técnico de mantenimiento <b>{self.data['evento']['Tecnico']}</b>, en la planta {self.data['evento']['Planta']}."
        self.elements.append(CondPageBreak(10))
        self.elements.append(Spacer(5, 0))
        self.elements.append(Paragraph(body_text, self.styles['Normal']))

        # Section 1: Registro de la Avería
        self.elements.append(CondPageBreak(10))
        self.elements.append(Spacer(5, 0))
        add_section_divider(self.elements, "Datos Informativos")
        #self.elements.append(Paragraph("<b>1. Registro de la Avería</b>", self.styles['Heading2']))
        
        
        table_data = [
            ['Fecha del evento', self.data['evento']['Fecha_Evento']],
            ['Categoría', self.data['evento']['Categoria']],
            ['Orden de Trabajo de la avería', self.data['evento']['OT_Averia']],
            ['Orden de Trabajo para RCA', self.data['evento']['OT_RCA']],
            ['Ubicación de la avería', self.data['evento']['Linea_Produccion']],
            ['Área', self.data['evento']['Area_Empresa']],
            ['Equipo', f"{self.data['evento']['Cod_SAP']} {self.data['evento']['Nombre_Equipo_SAP']}"],
            ['Parada de Línea', f"{self.data['evento']['Tiempo_Total']} hr(s) de parada de línea"]
        ]
        
        try:
            if self.data['evento']['Costos'] > 0:
                table_data.append(['Costos', f"${self.data['evento']['Costos']}"])
        except:
            pass
        try:
            if self.data['evento']['MTBF'] > 0:
                table_data.append(['Tiempo medio entre fallas (MTBF)', f"${self.data['evento']['MTBF']}"])
        except:
            pass
        try:
            if self.data['evento']['MTTR'] > 0:
                table_data.append(['Tiempo medio de reparación (MTTR)', f"${self.data['evento']['MTTR']}"])
        except:
            pass
        
        
        # Add table to the PDF
        table = Table(table_data, colWidths=[2.75*inch, 3*inch],hAlign='LEFT')
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear todo el contenido a la izquierda
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente normal
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente más pequeño
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),  # Espaciado inferior pequeño
            ('TOPPADDING', (0, 0), (-1, -1), 1),  # Espaciado superior pequeño
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))

        # Ajustar el ancho de las columnas: las respuestas tienen más espacio
        table._argW[0] = 160  # Ancho fijo para la columna de encabezados
        table._argW[1] = 300  # Ancho más grande para las respuestas       

        self.elements.append(table)
        self.elements.append(CondPageBreak(10))
        self.elements.append(Spacer(5, 0))
        add_section_divider(self.elements, "Descripción de la Avería")
        if self.data['problema']:
                          
            table_data_problem = []  # Crear una función auxiliar para obtener valores seguros

            if is_valid(self.data['problema']['Componente']):
                table_data_problem.append(['¿Qué componente?', Paragraph(self.data['problema']['Componente'],self.styles['Normal'])])
            if is_valid(self.data['problema']['Parte_de_Componente']):
                table_data_problem.append(['¿Qué parte del componente?', Paragraph(self.data['problema']['Parte_de_Componente'],self.styles['Normal'])])
            if is_valid(self.data['problema']['Difiere_estado_normal']):
                table_data_problem.append(['¿Cómo difiere de su estado normal?', Paragraph(self.data['problema']['Difiere_estado_normal'],self.styles['Normal'])])
    
           
            if self.data['problema']['Problema_previo'] =="Si, ha existido un problema previo":
                table_data_problem.append(['Descripción de sintoma previo', Paragraph(self.data['problema']['Detalles_Problema_Previo'],self.styles['Normal'])])
            if self.data['problema']['Problema_repetitivo'] == "Si, es repetitivo":
                table_data_problem.append(['Detalles de problema y repetitivo', Paragraph(self.data['problema']['Detalles_Problema_repetitivo'],self.styles['Normal'])])

            table_problem = Table(table_data_problem, colWidths=[2*inch, 3*inch],hAlign='LEFT')
            table_problem.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear todo el contenido a la izquierda
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente normal
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente más pequeño
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),  # Espaciado inferior pequeño
                ('TOPPADDING', (0, 0), (-1, -1), 1),  # Espaciado superior pequeño
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('WORDWRAP', (0, 0), (-1, -1), 1),  # Ajuste de línea automático
            ]))

            table_problem._argW[0] = 200  # Ancho fijo para la columna de encabezados
            table_problem._argW[1] = 300  # Ancho más grande para las respuesta
            self.elements.append(table_problem)
        else:
            noDescripciondeHechos = Paragraph("No se encuentra una descripción de los hechos", self.styles['Normal'])
            self.elements.append(noDescripciondeHechos)




        def create_equipment_table(equipment_data):
            """Genera la tabla con la información del equipo."""
            table_data = []
            
            # Validación de los datos
            def safe_get(key):
                return equipment_data.get(key) if is_valid(equipment_data.get(key)) else None

            # Datos del equipo
            fields = [
                ("Nombre del Equipo", safe_get("Nombre")),
                ("Fabricante", safe_get("Fabricante")),
                ("Detalles Técnicos", Paragraph(safe_get("Detalles_Tecnicos"),self.styles['Normal']))
            ]

            for label, value in fields:
                if value:
                    table_data.append([label, value])

            # Imagen del equipo
            image_path = safe_get("Imagen")
            if image_path:
                try:
                    img_path = os.path.join(os.getcwd(), image_path[1:])
                    image = Image(img_path, width=100, height=100)
                except Exception as e:
                    print(f"Error al cargar la imagen: {e}")
                    image = "No disponible"
                table_data.append(["Imagen del equipo", image])

            # Si no hay datos, devuelve None
            if not table_data:
                return None

            # Creación de la tabla
            table = Table(table_data, colWidths=[120, 300], hAlign='LEFT')
            
            # Estilos de la tabla
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Solo los títulos en negrita
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('WORDWRAP', (0, 0), (-1, -1), 1),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),  # Bordes sutiles
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#F2F2F2")),  # Fondo gris claro para la primera columna
            ]))

            return table

        # Sección de la descripción del equipo
        self.elements.append(CondPageBreak(10))
        self.elements.append(Spacer(5, 0))
        add_section_divider(self.elements, "Descripción del equipo")

        # Verificar si hay datos del equipo
        if self.data.get("equipo"):
            table_equipo = create_equipment_table(self.data["equipo"])
            if table_equipo:
                self.elements.append(Spacer(5, 0))
                self.elements.append(table_equipo)
                self.elements.append(CondPageBreak(10))
            else:
                no_equipo = Paragraph("No hay información disponible del equipo.", self.styles["Normal"])
                self.elements.append(no_equipo)
        else:
            no_equipo = Paragraph("No se encuentra una descripción del equipo", self.styles["Normal"])
            self.elements.append(no_equipo)

        
        self.elements.append(Spacer(5, 12))
        add_sub_section_divider(self.elements, "Condiciones de Funcionamiento")

        if self.data.get('condiciones') or self.data.get('secuencia'):
            # Create table for sequence
            texto_secuencia="Las condiciones de operación y las secuencias de funcionamiento del equipo están a continuación:"
            secuencia_paragraph = Paragraph(texto_secuencia, self.styles['Normal'])

            self.elements.append(secuencia_paragraph)
            self.elements.append(CondPageBreak(10))
            
            
            # Preparar datos para la tabla
            table_data_sequences = [['N° Sec',"Secuencia", "N° Cond", "Condición", "Imagen"]]  # Encabezados

            # Construir las filas de la tsabla
            for sequence in self.data['secuencia']:
                seq_conditions = [c for c in self.data['condiciones'] if c['Secuencia'] == sequence['Indice']]
                for condition in seq_conditions:
                    # Imagen opcional
                    if condition['Imagen']:
                        img = Image(os.path.join(os.getcwd(), condition['Imagen'][1:]), width=50, height=50)
                    else:
                        img = "No disponible"

                    # Fila de datos
                    table_data_sequences.append([
                        f"{sequence['Indice']}" ,
                        Paragraph(f"{sequence['Nombre']}",self.styles['Normal']),
                        f"{condition['Indice']}",
                        Paragraph(condition['Descripcion'],self.styles['Normal']),                        
                        img
                    ])

            # Crear tabla
            print(table_data_sequences)
            table_sequences = Table(table_data_sequences, colWidths=[50, 100,50, 200, 75], rowHeights=50)

            # Estilo de la tabla
            table_sequences.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),  # Bordes
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),  # Fondo de encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrado horizontal
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrado vertical
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),  # Negrita para encabezados
            ]))
            self.elements.append(Spacer(5, 12))
            self.elements.append(table_sequences)
            self.elements.append(CondPageBreak(10))
        else:
            noDescripciondeHechos = Paragraph("No existen condiciones de secuencias de funcionamiento planteadas para la avería", self.styles['Normal'])
            self.elements.append(noDescripciondeHechos)

        
        self.elements.append(Spacer(5, 0))
        # Sección: Descripción de los hechos
        add_section_divider(self.elements, "Descripción de los hechos")
        self.elements.append(CondPageBreak(10))

        if self.data.get('fenomeno'):
            # Tabla con preguntas y respuestas
            table_data_hechos = [['Pregunta', 'Respuesta']]
            if is_valid(self.data['fenomeno']['Que']):
                table_data_hechos.append([Paragraph('¿Qué? (Sistema que presento la avería)', self.styles['Normal']), Paragraph(self.data['fenomeno']['Que'], self.styles['Normal'])])
            if is_valid(self.data['fenomeno']['Cuando']):
                table_data_hechos.append([Paragraph('¿Cuando? (¿En que momento se rompe secuencia de funcionamiento?)', self.styles['Normal']), Paragraph(self.data['fenomeno']['Cuando'], self.styles['Normal'])])
            if is_valid(self.data['fenomeno']['Donde']):
                table_data_hechos.append([Paragraph('¿Dónde? Parte averiada específica de la máquina', self.styles['Normal']), Paragraph(self.data['fenomeno']['Donde'], self.styles['Normal'])])
            if is_valid(self.data['fenomeno']['Cual']):
                table_data_hechos.append([Paragraph('¿Cuál? Existe alguna tendencia o al azar', self.styles['Normal']), Paragraph(self.data['fenomeno']['Cual'], self.styles['Normal'])])
            if is_valid(self.data['fenomeno']['Quien']):
                table_data_hechos.append([Paragraph('¿Quién? (Depende de la habilidad de cada persona)', self.styles['Normal']), Paragraph(self.data['fenomeno']['Quien'], self.styles['Normal'])])
            if is_valid(self.data['fenomeno']['Como']):
                table_data_hechos.append([Paragraph('¿Cómo? ¿Como se evidencia la pieza averiada? (Fuga, rotura, quemado)', self.styles['Normal']), Paragraph(self.data['fenomeno']['Como'], self.styles['Normal'])])
            
            table_hechos = Table(table_data_hechos, colWidths=[2*inch, 2*inch], hAlign='LEFT')
            table_hechos.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('WORDWRAP', (0, 0), (-1, -1), 1),
            ]))
            # Ajuste de anchos para columnas específicas
            table_hechos._argW[0] = 160  # Encabezados
            table_hechos._argW[1] = 300  # Respuestas

            self.elements.append(Spacer(5, 0))
            self.elements.append(table_hechos)
            self.elements.append(CondPageBreak(10))
            self.elements.append(Spacer(5, 0))
            self.elements.append(Spacer(5, 0))
            self.elements.append(Spacer(5, 0))
            
            # Descripción de los hechos en un cuadrito
            if is_valid(self.data['fenomeno']['Detalles_de_los_hechos']):
                detalles_text = '<b>Descripción de los hechos:</b> ' + self.data.get('fenomeno', {}).get('Detalles_de_los_hechos', '')
                descripcion_paragraph = Paragraph(detalles_text, self.styles['Normal'])
                
                # Envolver el párrafo en una tabla para crear el efecto "cuadro"
                box_data = [[descripcion_paragraph]]
                box_table = Table(box_data, colWidths=[460])  # Ajusta el ancho según tu diseño
                
                box_table.setStyle(TableStyle([
                    ('BOX', (0, 0), (-1, -1), 1, colors.grey),           # Borde del cuadro
                    ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),   # Fondo muy suave
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),                  # Espacio interno a la izquierda
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),                 # Espacio interno a la derecha
                    ('TOPPADDING', (0, 0), (-1, -1), 6),                   # Espacio interno arriba
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),                # Espacio interno abajo
                ]))
                
                self.elements.append(box_table)
                self.elements.append(CondPageBreak(10))
        else:
            noDescripciondeHechos = Paragraph("No se encuentra una descripción de los hechos", self.styles['Normal'])
            self.elements.append(noDescripciondeHechos)
        
        self.elements.append(Spacer(5, 0))

        add_section_divider(self.elements, "Método Cinco Porque")
        self.elements.append(CondPageBreak(10))
        if self.data.get('cincoporque'):
                # Crear una función auxiliar para obtener valores seguros
                def get_safe_value(key):
                    value = self.data['cincoporque'].get(key)
                    return value if value else ""  # Devuelve cadena vacía si el valor es None o no existe

                table_data_hechos = [
                    ['Pregunta', 'Respuesta'],
                    [Paragraph(get_safe_value('Primer_porque'), first_col_style), Paragraph(get_safe_value('Primera_respuesta'), self.styles['Normal'])],
                    [Paragraph(get_safe_value('Segundo_porque'),first_col_style), Paragraph(get_safe_value('Segunda_respuesta'), self.styles['Normal'])],
                    [Paragraph(get_safe_value('Tercer_porque'), first_col_style), Paragraph(get_safe_value('Tercera_respuesta'), self.styles['Normal'])],
                    [Paragraph(get_safe_value('Cuarto_porque'), first_col_style), Paragraph(get_safe_value('Cuarta_respuesta'), self.styles['Normal'])],
                    [Paragraph(get_safe_value('Quinto_porque'), first_col_style), Paragraph(get_safe_value('Quinta_respuesta'), self.styles['Normal'])],
                ]

                table_hechos = Table(table_data_hechos, colWidths=[2 * inch, 2 * inch], hAlign='LEFT')
                table_hechos.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear todo el contenido a la izquierda
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente normal
                    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente más pequeño
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),  # Espaciado inferior pequeño
                    ('TOPPADDING', (0, 0), (-1, -1), 1),  # Espaciado superior pequeño
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('WORDWRAP', (0, 0), (-1, -1), 1),  # Ajuste de línea automático
                ]))

             
                table_hechos._argW[0] = 200  # Ancho fijo para la columna de encabezados
                table_hechos._argW[1] = 250  # Ancho más grande para las respuesta
                self.elements.append(Spacer(5, 0))
                self.elements.append(table_hechos)
                self.elements.append(CondPageBreak(10))
                self.elements.append(Spacer(5, 0))
                            # Descripción de los hechos en un cuadrito
                if is_valid(self.data['cincoporque']['Tipo_de_averia']):
                    detalles_text = '<b>Tipo de Avería:  </b> ' + self.data.get('cincoporque', {}).get('Tipo_de_averia', '')
                    descripcion_paragraph = Paragraph(detalles_text, self.styles['Normal'])
                    
                    # Envolver el párrafo en una tabla para crear el efecto "cuadro"
                    box_data = [[descripcion_paragraph]]
                    box_table = Table(box_data, colWidths=[460])  # Ajusta el ancho según tu diseño
                    
                    box_table.setStyle(TableStyle([
                        ('BOX', (0, 0), (-1, -1), 1, colors.grey),           # Borde del cuadro
                        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),   # Fondo muy suave
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),                  # Espacio interno a la izquierda
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),                 # Espacio interno a la derecha
                        ('TOPPADDING', (0, 0), (-1, -1), 6),                   # Espacio interno arriba
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),                # Espacio interno abajo
                    ]))
                    
                    self.elements.append(box_table)
                    self.elements.append(CondPageBreak(10))
                else:
                    noDescripciondeHechos = Paragraph("No se encuentra una análisis de cinco porques", self.styles['Normal'])
                    self.elements.append(noDescripciondeHechos)
                        


        self.elements.append(Spacer(5, 12))
        add_section_divider(self.elements, "Contramedidas")
        if self.data.get('contramedidas'):
            texto_contramedidas="Las contramedidas para completar el ciclo de no recurrencia son:"
            contramedidas_paragraph = Paragraph(texto_contramedidas, self.styles['Normal'])
            self.elements.append(contramedidas_paragraph)
            self.elements.append(CondPageBreak(10))  
                    # Preparar datos para la tabla
            table_data_contramedidas = [['Tipo',"Descripción Breve", "OT", "Fecha", "Cumplimiento"]]  # Encabezados

            # Construir las filas de la tsabla
            for contramedida in self.data['contramedidas']:
                if f"{contramedida['OT_Completado']}"=="on":
                    contramedida_estado="Completado"
                else:
                    contramedida_estado="Pendiente"
                table_data_contramedidas.append([
                    Paragraph(f"{contramedida['Tipo']}" ,self.styles['Normal']),
                    Paragraph(f"{contramedida['Descripcion_breve']}",self.styles['Normal']),
                    f"{contramedida['OT_SAP']}",
                    f"{contramedida['Fecha_de_cumplimiento']}",
                    contramedida_estado,
                ])

            # Crear tabla
            table_contramedidas = Table(table_data_contramedidas, colWidths=[100, 130,70, 100, 75], rowHeights=50)

            # Estilo de la tabla
            table_contramedidas.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),  # Bordes
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),  # Fondo de encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrado horizontal
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrado vertical
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),  # Negrita para encabezados# Negrita para encabezados
            ]))
            self.elements.append(Spacer(5, 12))
            self.elements.append(table_contramedidas)
            self.elements.append(CondPageBreak(10))
        else:
            noDescripciondeHechos = Paragraph("No existen contramedidas planteadas para la avería", self.styles['Normal'])
            self.elements.append(noDescripciondeHechos)
        
        self.elements.append(CondPageBreak(10))
        self.elements.append(Spacer(5, 0))
        add_section_divider(self.elements, "Realizado por:")
        table_data_autores=[]
        if is_valid(self.data['evento'].get('Autor')):
            table_data_autores.append(['Realizado por:', self.data['evento']['Autor']])
        if is_valid(self.data['evento'].get('Autor')):
            table_data_autores.append(['Técnico(s) que atendió la avería:', self.data['evento']['Tecnico']])
        if is_valid(self.data['evento'].get('Tecnico')):
            table_data_autores.append(['Representante de Mantenimiento', self.data['evento']['Representante_Mantenimiento']])
        if is_valid(self.data['evento'].get('Representante_Produccion')):
            table_data_autores.append(['Representante de Mantenimiento', self.data['evento']['Representante_Produccion']])
        if is_valid(self.data['evento'].get('Representante_SASS')):
            table_data_autores.append(['Representante de EHS', self.data['evento']['Representante_SASS']])
        if is_valid(self.data['evento'].get('Representante_Calidad')):
            table_data_autores.append(['Representante de Calidad', self.data['evento']['Representante_Calidad']])


        table_autores = Table(table_data_autores,  colWidths=[200, 300], hAlign='LEFT')
        table_autores.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear todo el contenido a la izquierda
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente normal
                    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente más pequeño
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),  # Espaciado inferior pequeño
                    ('TOPPADDING', (0, 0), (-1, -1), 1),  # Espaciado superior pequeño
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('WORDWRAP', (0, 0), (-1, -1), 1),  # Ajuste de línea automático
                ]))
        self.elements.append(Spacer(5, 12))
        self.elements.append(table_autores)

        
        self.elements.append(Spacer(5, 0))
        add_section_divider(self.elements, "Anexos Imágenes de Avería")
        
        # Insert image
        for fotos in self.data['imagen_averia']:
            relative_path = fotos['Imagen_de_Averia']
            img_path = os.path.join(os.getcwd(), relative_path[1:])
            if os.path.exists(img_path):
                img = Image(img_path, width=200, height=200)
                self.elements.append(Spacer(5, 0))
                self.elements.append(img)
                self.elements.append(Spacer(5, 0))
            else:
                print("no existe ruta")
      
  