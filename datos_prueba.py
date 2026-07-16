"""
datos_prueba.py
----------------
"Base de datos" de prueba. Reemplaza PERSONAS_DE_PRUEBA por el
resultado real de tu consulta (SQL, API, CSV, JSON...) y todo lo
demás (capas, layout, animación) se recalcula solo.

Cada registro es un diccionario con este formato:

    id                str   -> identificador único
    nombre            str   -> nombre de pila
    apellido          str   -> apellido(s)
    descripcion       str   -> reseña / biografía de la persona
    generacion        int   -> nivel en el árbol (0 = generación más antigua)
    genero            str   -> 'M' (masculino) o 'F' (femenino)
    año_nacimiento    int   -> año en que nació la persona
    padres_ids        list  -> ids de sus padres (exactamente 2, heterosexuales, casados). Opcional.
    pareja_id         str   -> id de su pareja, para dibujar el enlace. Opcional.
    inmune_gripe      float -> inmunidad a la gripe (0.0 a 1.0)
    inmune_covid      float -> inmunidad al COVID-19 (0.0 a 1.0)
    inmune_bacteria   float -> inmunidad a infecciones bacterianas (0.0 a 1.0)
"""

PERSONAS_DE_PRUEBA = [
    # ---- generación 0: bisabuelos ----
    {
        "id": "p1", "nombre": "Rosario", "apellido": "Núñez Ibarra", "generacion": 0,
        "genero": "F", "año_nacimiento": 1934, "pareja_id": "p2", "padres_ids": [],
        "inmune_gripe": 0.20, "inmune_covid": 0.15, "inmune_bacteria": 0.30,
        "descripcion": "Nacida en 1934 en las faldas de la cordillera. Junto a Efraín levantó "
                        "la primera finca cafetera de la familia y crió a sus hijos entre "
                        "los cafetales.",
    },
    {
        "id": "p2", "nombre": "Efraín", "apellido": "Camacho Duarte", "generacion": 0,
        "genero": "M", "año_nacimiento": 1931, "pareja_id": "p1", "padres_ids": [],
        "inmune_gripe": 0.15, "inmune_covid": 0.10, "inmune_bacteria": 0.25,
        "descripcion": "Arriero de oficio antes de asentarse. Compró las primeras hectáreas "
                        "de tierra en 1958 y las convirtió en el corazón de la finca familiar.",
    },

    # ---- generación 1: abuelos ----
    {
        "id": "p3", "nombre": "Marta", "apellido": "Camacho Núñez", "generacion": 1,
        "genero": "F", "año_nacimiento": 1958, "pareja_id": "p4", "padres_ids": ["p1", "p2"],
        "inmune_gripe": 0.40, "inmune_covid": 0.35, "inmune_bacteria": 0.45,
        "descripcion": "Primera hija de Rosario y Efraín. Estudió magisterio y fundó la "
                        "escuela veredal donde enseñó durante treinta años.",
    },
    {
        "id": "p4", "nombre": "Héctor", "apellido": "Salgado Prieto", "generacion": 1,
        "genero": "M", "año_nacimiento": 1956, "pareja_id": "p3", "padres_ids": [],
        "inmune_gripe": 0.45, "inmune_covid": 0.40, "inmune_bacteria": 0.50,
        "descripcion": "Llegó al pueblo como veterinario itinerante y se quedó para siempre "
                        "tras casarse con Marta en 1975.",
    },
    {
        "id": "p5", "nombre": "Rodrigo", "apellido": "Camacho Núñez", "generacion": 1,
        "genero": "M", "año_nacimiento": 1961, "pareja_id": "p6", "padres_ids": ["p1", "p2"],
        "inmune_gripe": 0.55, "inmune_covid": 0.50, "inmune_bacteria": 0.60,
        "descripcion": "Segundo hijo de Rosario y Efraín. Modernizó el cultivo de café con "
                        "nuevas técnicas de secado.",
    },
    {
        "id": "p6", "nombre": "Lucía", "apellido": "Fernández Soto", "generacion": 1,
        "genero": "F", "año_nacimiento": 1964, "pareja_id": "p5", "padres_ids": [],
        "inmune_gripe": 0.60, "inmune_covid": 0.55, "inmune_bacteria": 0.65,
        "descripcion": "Contadora de profesión. Llevó las cuentas de la finca durante "
                        "décadas y fue quien impulsó la primera exportación de café.",
    },

    # ---- generación 2: padres ----
    {
        "id": "p7", "nombre": "Daniela", "apellido": "Salgado Camacho", "generacion": 2,
        "genero": "F", "año_nacimiento": 1988, "pareja_id": "p13", "padres_ids": ["p3", "p4"],
        "inmune_gripe": 0.70, "inmune_covid": 0.68, "inmune_bacteria": 0.75,
        "descripcion": "Hija mayor de Marta y Héctor. Estudió arquitectura y hoy diseña las "
                        "etiquetas de café que exporta la familia.",
    },
    {
        "id": "p13", "nombre": "Santiago", "apellido": "Castro Ortiz", "generacion": 2,
        "genero": "M", "año_nacimiento": 1986, "pareja_id": "p7", "padres_ids": [],
        "inmune_gripe": 0.72, "inmune_covid": 0.70, "inmune_bacteria": 0.73,
        "descripcion": "Agrónomo apasionado que se integró a la familia aportando sus "
                        "conocimientos en el control biológico de plagas.",
    },
    {
        "id": "p8", "nombre": "Andrés", "apellido": "Salgado Camacho", "generacion": 2,
        "genero": "M", "año_nacimiento": 1984, "pareja_id": "p9", "padres_ids": ["p3", "p4"],
        "inmune_gripe": 0.65, "inmune_covid": 0.60, "inmune_bacteria": 0.70,
        "descripcion": "Se quedó en la finca y hoy dirige la producción. Reconocido en la "
                        "región por sus catas de café.",
    },
    {
        "id": "p9", "nombre": "Paula", "apellido": "Ríos Medina", "generacion": 2,
        "genero": "F", "año_nacimiento": 1986, "pareja_id": "p8", "padres_ids": [],
        "inmune_gripe": 0.80, "inmune_covid": 0.78, "inmune_bacteria": 0.82,
        "descripcion": "Bióloga especializada en suelos. Llegó a la finca por trabajo y se "
                        "quedó para siempre junto a Andrés.",
    },
    {
        "id": "p10", "nombre": "Sebastián", "apellido": "Camacho Fernández", "generacion": 2,
        "genero": "M", "año_nacimiento": 1991, "pareja_id": "p15", "padres_ids": ["p5", "p6"],
        "inmune_gripe": 0.75, "inmune_covid": 0.72, "inmune_bacteria": 0.78,
        "descripcion": "Hijo de Rodrigo y Lucía. Hoy cuenta la historia de la familia "
                        "en un podcast sobre cafeteros colombianos.",
    },
    {
        "id": "p15", "nombre": "Gabriela", "apellido": "Gómez Díaz", "generacion": 2,
        "genero": "F", "año_nacimiento": 1993, "pareja_id": "p10", "padres_ids": [],
        "inmune_gripe": 0.78, "inmune_covid": 0.75, "inmune_bacteria": 0.80,
        "descripcion": "Diseñadora web que ayuda a digitalizar el comercio de la cooperativa "
                        "familiar y la distribución internacional.",
    },
    {
        "id": "p17", "nombre": "Mariana", "apellido": "Camacho Fernández", "generacion": 2,
        "genero": "F", "año_nacimiento": 1994, "pareja_id": "p18", "padres_ids": ["p5", "p6"],
        "inmune_gripe": 0.82, "inmune_covid": 0.80, "inmune_bacteria": 0.85,
        "descripcion": "Hija menor de Rodrigo y Lucía. Es médica pediatra y apoya a las "
                        "comunidades rurales del municipio con jornadas de salud.",
    },
    {
        "id": "p18", "nombre": "Gabriel", "apellido": "Morales Torres", "generacion": 2,
        "genero": "M", "año_nacimiento": 1992, "pareja_id": "p17", "padres_ids": [],
        "inmune_gripe": 0.80, "inmune_covid": 0.75, "inmune_bacteria": 0.82,
        "descripcion": "Ingeniero ambiental que colabora con Mariana en la implementación "
                        "de proyectos de agua potable para las escuelas locales.",
    },

    # ---- generación 3: hijos ----
    {
        "id": "p11", "nombre": "Mateo", "apellido": "Salgado Ríos", "generacion": 3,
        "genero": "M", "año_nacimiento": 2010, "padres_ids": ["p8", "p9"],
        "inmune_gripe": 0.85, "inmune_covid": 0.80, "inmune_bacteria": 0.88,
        "descripcion": "El más joven con carné de catador oficial. Sueña con abrir su "
                        "propia cafetería usando el grano de la finca.",
    },
    {
        "id": "p12", "nombre": "Valentina", "apellido": "Salgado Ríos", "generacion": 3,
        "genero": "F", "año_nacimiento": 2006, "padres_ids": ["p8", "p9"],
        "inmune_gripe": 0.90, "inmune_covid": 0.85, "inmune_bacteria": 0.92,
        "descripcion": "Estudia ingeniería agrícola; diseñó el nuevo sistema de riego de la "
                        "finca para su proyecto de grado.",
    },
    {
        "id": "p14", "nombre": "Diana", "apellido": "Castro Salgado", "generacion": 3,
        "genero": "F", "año_nacimiento": 2013, "padres_ids": ["p7", "p13"],
        "inmune_gripe": 0.88, "inmune_covid": 0.82, "inmune_bacteria": 0.86,
        "descripcion": "Hija de Daniela y Santiago. Le encanta pintar aves locales y su "
                        "sueño es ilustrar un libro sobre la fauna de los cafetales.",
    },
    {
        "id": "p16", "nombre": "Sofía", "apellido": "Camacho Gómez", "generacion": 3,
        "genero": "F", "año_nacimiento": 2018, "padres_ids": ["p10", "p15"],
        "inmune_gripe": 0.84, "inmune_covid": 0.80, "inmune_bacteria": 0.82,
        "descripcion": "Hija pequeña de Sebastián y Gabriela. Acompaña a sus abuelos por "
                        "la finca recogiendo semillas e inventando canciones.",
    },
    {
        "id": "p19", "nombre": "Lucas", "apellido": "Morales Camacho", "generacion": 3,
        "genero": "M", "año_nacimiento": 2019, "padres_ids": ["p17", "p18"],
        "inmune_gripe": 0.86, "inmune_covid": 0.82, "inmune_bacteria": 0.84,
        "descripcion": "Hijo menor de Mariana y Gabriel. Muy curioso e hiperactivo, le "
                        "encanta descubrir insectos bajo la supervisión de sus padres.",
    },
]

ETIQUETAS_GENERACION = {0: "Bisabuelos", 1: "Abuelos", 2: "Padres", 3: "Hijos"}
