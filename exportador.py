"""
exportador.py
-------------
Módulo encargado de generar reportes impresos en formato PDF para el Árbol Genealógico
y Análisis de Teoría de Grafos usando ReportLab.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import datetime


def generar_reporte_pdf(arbol, filepath, titulo_familia="Familia Camacho Núñez"):
    """
    Genera un informe completo en PDF a partir de un objeto ArbolGenealogico.
    Devuelve True si el archivo se creó correctamente.
    """
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Definir estilos personalizados
    style_titulo = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#12201A"),
        spaceAfter=6
    )

    style_subtitulo = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#5A4C36"),
        spaceAfter=14
    )

    style_sec_header = ParagraphStyle(
        'SecHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#C9A227"),
        spaceBefore=12,
        spaceAfter=6
    )

    style_cuerpo = ParagraphStyle(
        'CuerpoText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2B2118"),
        spaceAfter=4
    )

    style_tabla_hdr = ParagraphStyle(
        'TablaHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1 # centrado
    )

    style_tabla_celda = ParagraphStyle(
        'TablaCelda',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2B2118")
    )

    style_mono = ParagraphStyle(
        'MonoCelda',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#12201A")
    )

    story = []

    # 1. ENCABEZADO DEL DOCUMENTO
    story.append(Paragraph("REPORTE GENEALÓGICO Y ANÁLISIS DE GRAFOS", style_titulo))
    fecha_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<b>Árbol:</b> {titulo_familia} &nbsp;|&nbsp; <b>Fecha de generación:</b> {fecha_str}", style_subtitulo))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#C9A227"), spaceAfter=10))

    # 2. SECCIÓN: PROPIEDADES DISCRETAS Y DE TEORÍA DE GRAFOS
    story.append(Paragraph("1. ANÁLISIS DE TEORÍA DE GRAFOS Y MATEMÁTICAS DISCRETAS", style_sec_header))

    props = arbol.analizar_propiedades_discretas()
    total_nodos = props['nodos']
    total_aristas = props['aristas']
    es_dag = "Sí (Válido - Acíclico Dirigido)" if props['dag'] else "No (Posee ciclos)"
    es_conexo = "Sí (Toda la red está conectada)" if props['conexo'] else "No (Bosque con familias aisladas)"
    max_grado_txt = f"{props['max_grado_nombre']} (Grado total: {props['max_grado']})"
    euleriano_txt = "Existe recorrido euleriano" if props['euleriano'] else f"No existe ({props['cantidad_nodos_impares']} nodos de grado impar)"
    hamiltoniano_txt = "Existe camino hamiltoniano" if props['hamiltoniano'] else "No existe camino hamiltoniano"

    data_props = [
        [Paragraph("<b>Métrica / Propiedad</b>", style_tabla_hdr), Paragraph("<b>Resultado / Evaluación</b>", style_tabla_hdr)],
        [Paragraph("Total de Personas (Nodos V)", style_tabla_celda), Paragraph(str(total_nodos), style_tabla_celda)],
        [Paragraph("Total de Relaciones (Aristas E)", style_tabla_celda), Paragraph(str(total_aristas), style_tabla_celda)],
        [Paragraph("¿Es Grafo Acíclico Dirigido (DAG)?", style_tabla_celda), Paragraph(es_dag, style_tabla_celda)],
        [Paragraph("¿Es Grafo Conexo?", style_tabla_celda), Paragraph(es_conexo, style_tabla_celda)],
        [Paragraph("Persona con Mayor Grado", style_tabla_celda), Paragraph(max_grado_txt, style_tabla_celda)],
        [Paragraph("Camino Euleriano", style_tabla_celda), Paragraph(euleriano_txt, style_tabla_celda)],
        [Paragraph("Camino Hamiltoniano", style_tabla_celda), Paragraph(hamiltoniano_txt, style_tabla_celda)],
    ]

    t_props = Table(data_props, colWidths=[2.2 * inch, 4.8 * inch])
    t_props.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#1C2A21")),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F6EE")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_props)
    story.append(Spacer(1, 14))

    # 3. SECCIÓN: TABLA DETALLADA DE INTEGRANTES DE LA FAMILIA
    story.append(Paragraph("2. REGISTRO COMPLETO DE PERSONAS", style_sec_header))

    headers_personas = [
        Paragraph("<b>ID</b>", style_tabla_hdr),
        Paragraph("<b>Nombre Completo</b>", style_tabla_hdr),
        Paragraph("<b>Gen</b>", style_tabla_hdr),
        Paragraph("<b>Sex</b>", style_tabla_hdr),
        Paragraph("<b>Año</b>", style_tabla_hdr),
        Paragraph("<b>Inmunidades (G/C/B)</b>", style_tabla_hdr),
        Paragraph("<b>Padres / Pareja</b>", style_tabla_hdr)
    ]
    data_personas = [headers_personas]

    for n_id, nodo in arbol.nodos.items():
        nom_padres = ", ".join([p.nombre for p in nodo.padres]) if nodo.padres else "Sin reg."
        pareja_str = f" | Pareja: {nodo.pareja.nombre}" if nodo.pareja else ""
        rel_str = f"{nom_padres}{pareja_str}"
        inm_str = f"{int(nodo.inmune_gripe*100)}% / {int(nodo.inmune_covid*100)}% / {int(nodo.inmune_bacteria*100)}%"

        row = [
            Paragraph(nodo.id, style_tabla_celda),
            Paragraph(f"<b>{nodo.nombre_completo()}</b>", style_tabla_celda),
            Paragraph(str(nodo.generacion), style_tabla_celda),
            Paragraph("M" if nodo.genero == "M" else "F", style_tabla_celda),
            Paragraph(str(nodo.año_nacimiento), style_tabla_celda),
            Paragraph(inm_str, style_tabla_celda),
            Paragraph(rel_str, style_tabla_celda)
        ]
        data_personas.append(row)

    t_personas = Table(data_personas, colWidths=[0.5*inch, 1.8*inch, 0.4*inch, 0.4*inch, 0.5*inch, 1.4*inch, 2.0*inch])
    t_personas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1C2A21")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F6EE")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_personas)
    story.append(Spacer(1, 14))

    # 4. SECCIÓN: MATRIZ DE ADYACENCIA DIRIGIDA
    story.append(Paragraph("3. MATRIZ DE ADYACENCIA DIRIGIDA", style_sec_header))

    nodos_ids, matriz = arbol.generar_matriz_adyacencia()
    if nodos_ids:
        # Construir representación matricial en texto
        lineas_matriz = []
        nombres_cortos = [arbol.nodos[nid].nombre[:6] for nid in nodos_ids]
        hdr_txt = f"{'ID/Nom':<8}" + "".join([f"{nom:^6}" for nom in nombres_cortos])
        lineas_matriz.append(hdr_txt)
        lineas_matriz.append("-" * len(hdr_txt))

        for i, row in enumerate(matriz):
            r_str = f"{nombres_cortos[i]:<8}" + "".join([f"{val:^6}" for val in row])
            lineas_matriz.append(r_str)

        txt_matriz_full = "\n".join(lineas_matriz)
        story.append(Paragraph(f"<pre>{txt_matriz_full}</pre>", style_mono))

    doc.build(story)
    return True


def generar_reporte_comparacion_pdf(arbol1, arbol2, filepath, titulo1="Árbol 1 (Actual)", titulo2="Árbol 2 (Comparación)"):
    """
    Genera un informe comparativo en PDF entre dos objetos ArbolGenealogico.
    """
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    style_titulo = ParagraphStyle(
        'DocTitleComp',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#12201A"),
        spaceAfter=6
    )

    style_subtitulo = ParagraphStyle(
        'DocSubtitleComp',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#5A4C36"),
        spaceAfter=12
    )

    style_sec_header = ParagraphStyle(
        'SecHeaderComp',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#C9A227"),
        spaceBefore=12,
        spaceAfter=6
    )

    style_tabla_hdr = ParagraphStyle(
        'TablaHeaderComp',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    style_tabla_celda = ParagraphStyle(
        'TablaCeldaComp',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2B2118")
    )

    style_mono = ParagraphStyle(
        'MonoComp',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#12201A")
    )

    story = []

    # Header
    story.append(Paragraph("REPORTE COMPARATIVO DE ÁRBOLES Y GRAFOS", style_titulo))
    fecha_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<b>Comparando:</b> {titulo1} vs {titulo2} &nbsp;|&nbsp; <b>Fecha:</b> {fecha_str}", style_subtitulo))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#C9A227"), spaceAfter=10))

    comp = arbol1.comparar_con(arbol2)
    p1 = comp["arbol1"]
    p2 = comp["arbol2"]

    data_comp = [
        [Paragraph("<b>Métrica / Propiedad</b>", style_tabla_hdr),
         Paragraph(f"<b>{titulo1}</b>", style_tabla_hdr),
         Paragraph(f"<b>{titulo2}</b>", style_tabla_hdr),
         Paragraph("<b>Diferencia / Análisis</b>", style_tabla_hdr)],
        
        [Paragraph("Total Personas (Nodos V)", style_tabla_celda),
         Paragraph(str(p1['nodos']), style_tabla_celda),
         Paragraph(str(p2['nodos']), style_tabla_celda),
         Paragraph(f"{comp['diff_nodos']:+} nodo(s)", style_tabla_celda)],
        
        [Paragraph("Total Relaciones (Aristas E)", style_tabla_celda),
         Paragraph(str(p1['aristas']), style_tabla_celda),
         Paragraph(str(p2['aristas']), style_tabla_celda),
         Paragraph(f"{comp['diff_aristas']:+} arista(s)", style_tabla_celda)],
        
        [Paragraph("Densidad del Grafo", style_tabla_celda),
         Paragraph(str(comp['densidad1']), style_tabla_celda),
         Paragraph(str(comp['densidad2']), style_tabla_celda),
         Paragraph(f"{round(comp['densidad1'] - comp['densidad2'], 4):+}", style_tabla_celda)],

        [Paragraph("Grado Promedio", style_tabla_celda),
         Paragraph(str(comp['grado_promedio1']), style_tabla_celda),
         Paragraph(str(comp['grado_promedio2']), style_tabla_celda),
         Paragraph(f"{round(comp['grado_promedio1'] - comp['grado_promedio2'], 2):+}", style_tabla_celda)],

        [Paragraph("Grado Máximo", style_tabla_celda),
         Paragraph(f"{p1['max_grado_nombre']} ({p1['max_grado']})", style_tabla_celda),
         Paragraph(f"{p2['max_grado_nombre']} ({p2['max_grado']})", style_tabla_celda),
         Paragraph(f"Diff max: {p1['max_grado'] - p2['max_grado']:+}", style_tabla_celda)],

        [Paragraph("¿Es DAG (Acíclico)?", style_tabla_celda),
         Paragraph("Sí" if p1['dag'] else "No", style_tabla_celda),
         Paragraph("Sí" if p2['dag'] else "No", style_tabla_celda),
         Paragraph("Iguales" if p1['dag'] == p2['dag'] else "Diferentes", style_tabla_celda)],

        [Paragraph("¿Es Conexo?", style_tabla_celda),
         Paragraph("Sí" if p1['conexo'] else "No", style_tabla_celda),
         Paragraph("Sí" if p2['conexo'] else "No", style_tabla_celda),
         Paragraph("Iguales" if p1['conexo'] == p2['conexo'] else "Diferentes", style_tabla_celda)],

        [Paragraph("Camino Euleriano", style_tabla_celda),
         Paragraph("Sí" if p1['euleriano'] else "No", style_tabla_celda),
         Paragraph("Sí" if p2['euleriano'] else "No", style_tabla_celda),
         Paragraph("Iguales" if p1['euleriano'] == p2['euleriano'] else "Diferentes", style_tabla_celda)],

        [Paragraph("Camino Hamiltoniano", style_tabla_celda),
         Paragraph("Sí" if p1['hamiltoniano'] else "No", style_tabla_celda),
         Paragraph("Sí" if p2['hamiltoniano'] else "No", style_tabla_celda),
         Paragraph("Iguales" if p1['hamiltoniano'] == p2['hamiltoniano'] else "Diferentes", style_tabla_celda)],

        [Paragraph("Matriz: Conexiones (1s)", style_tabla_celda),
         Paragraph(str(comp['ones_matriz1']), style_tabla_celda),
         Paragraph(str(comp['ones_matriz2']), style_tabla_celda),
         Paragraph(f"{comp['ones_matriz1'] - comp['ones_matriz2']:+} conex.", style_tabla_celda)],
    ]

    t_comp = Table(data_comp, colWidths=[2.0 * inch, 1.7 * inch, 1.7 * inch, 1.6 * inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1C2A21")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F6EE")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    story.append(Paragraph("1. TABLA COMPARATIVA DE PROPIEDADES DISCRETAS", style_sec_header))
    story.append(t_comp)
    story.append(Spacer(1, 14))

    doc.build(story)
    return True

