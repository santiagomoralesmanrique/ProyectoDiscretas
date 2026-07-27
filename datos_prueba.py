# datos_prueba.py - datos iniciales de prueba para el arbol

PERSONAS_DE_PRUEBA = [
    # gen 0: bisabuelos
    {
        "id": "p1", "nombre": "Rosario", "apellido": "Núñez Ibarra", "generacion": 0,
        "genero": "F", "ano_nacimiento": 1934, "pareja_id": "p2", "padres_ids": [],
        "inmune_gripe": 0.20, "inmune_covid": 0.15, "inmune_bacteria": 0.30,
        "descripcion": "Nacida en 1934. Junto a Efraín levantó la primera finca de la familia."
    },
    {
        "id": "p2", "nombre": "Efraín", "apellido": "Camacho Duarte", "generacion": 0,
        "genero": "M", "ano_nacimiento": 1931, "pareja_id": "p1", "padres_ids": [],
        "inmune_gripe": 0.15, "inmune_covid": 0.10, "inmune_bacteria": 0.25,
        "descripcion": "Agricultor y fundador de la finca principal."
    },

    # gen 1: abuelos
    {
        "id": "p3", "nombre": "Marta", "apellido": "Camacho Núñez", "generacion": 1,
        "genero": "F", "ano_nacimiento": 1958, "pareja_id": "p4", "padres_ids": ["p1", "p2"],
        "inmune_gripe": 0.40, "inmune_covid": 0.35, "inmune_bacteria": 0.45,
        "descripcion": "Profesora de escuela veredal, hija de Rosario y Efraín."
    },
    {
        "id": "p4", "nombre": "Héctor", "apellido": "Salgado Prieto", "generacion": 1,
        "genero": "M", "ano_nacimiento": 1956, "pareja_id": "p3", "padres_ids": [],
        "inmune_gripe": 0.45, "inmune_covid": 0.40, "inmune_bacteria": 0.50,
        "descripcion": "Veterinario del pueblo, casado con Marta."
    },
    {
        "id": "p5", "nombre": "Rodrigo", "apellido": "Camacho Núñez", "generacion": 1,
        "genero": "M", "ano_nacimiento": 1961, "pareja_id": "p6", "padres_ids": ["p1", "p2"],
        "inmune_gripe": 0.55, "inmune_covid": 0.50, "inmune_bacteria": 0.60,
        "descripcion": "Cafetero dedicado a administrar los terrenos familiares."
    },
    {
        "id": "p6", "nombre": "Lucía", "apellido": "Fernández Soto", "generacion": 1,
        "genero": "F", "ano_nacimiento": 1964, "pareja_id": "p5", "padres_ids": [],
        "inmune_gripe": 0.60, "inmune_covid": 0.55, "inmune_bacteria": 0.65,
        "descripcion": "Contadora del negocio familiar."
    },

    # gen 2: padres
    {
        "id": "p7", "nombre": "Daniela", "apellido": "Salgado Camacho", "generacion": 2,
        "genero": "F", "ano_nacimiento": 1988, "pareja_id": "p13", "padres_ids": ["p3", "p4"],
        "inmune_gripe": 0.70, "inmune_covid": 0.68, "inmune_bacteria": 0.75,
        "descripcion": "Arquitecta, trabaja en proyectos locales."
    },
    {
        "id": "p13", "nombre": "Santiago", "apellido": "Castro Ortiz", "generacion": 2,
        "genero": "M", "ano_nacimiento": 1986, "pareja_id": "p7", "padres_ids": [],
        "inmune_gripe": 0.72, "inmune_covid": 0.70, "inmune_bacteria": 0.73,
        "descripcion": "Ingeniero agronomo."
    },
    {
        "id": "p8", "nombre": "Andrés", "apellido": "Salgado Camacho", "generacion": 2,
        "genero": "M", "ano_nacimiento": 1984, "pareja_id": "p9", "padres_ids": ["p3", "p4"],
        "inmune_gripe": 0.65, "inmune_covid": 0.60, "inmune_bacteria": 0.70,
        "descripcion": "Administrador de la finca y cafetero."
    },
    {
        "id": "p9", "nombre": "Paula", "apellido": "Ríos Medina", "generacion": 2,
        "genero": "F", "ano_nacimiento": 1986, "pareja_id": "p8", "padres_ids": [],
        "inmune_gripe": 0.80, "inmune_covid": 0.78, "inmune_bacteria": 0.82,
        "descripcion": "Biologa de la universidad local."
    },
    {
        "id": "p10", "nombre": "Sebastián", "apellido": "Camacho Fernández", "generacion": 2,
        "genero": "M", "ano_nacimiento": 1991, "pareja_id": "p15", "padres_ids": ["p5", "p6"],
        "inmune_gripe": 0.75, "inmune_covid": 0.72, "inmune_bacteria": 0.78,
        "descripcion": "Comerciante independiente."
    },
    {
        "id": "p15", "nombre": "Gabriela", "apellido": "Gómez Díaz", "generacion": 2,
        "genero": "F", "ano_nacimiento": 1993, "pareja_id": "p10", "padres_ids": [],
        "inmune_gripe": 0.78, "inmune_covid": 0.75, "inmune_bacteria": 0.80,
        "descripcion": "Diseñadora de sistemas."
    },
    {
        "id": "p17", "nombre": "Mariana", "apellido": "Camacho Fernández", "generacion": 2,
        "genero": "F", "ano_nacimiento": 1994, "pareja_id": "p18", "padres_ids": ["p5", "p6"],
        "inmune_gripe": 0.82, "inmune_covid": 0.80, "inmune_bacteria": 0.85,
        "descripcion": "Medica general."
    },
    {
        "id": "p18", "nombre": "Gabriel", "apellido": "Morales Torres", "generacion": 2,
        "genero": "M", "ano_nacimiento": 1992, "pareja_id": "p17", "padres_ids": [],
        "inmune_gripe": 0.80, "inmune_covid": 0.75, "inmune_bacteria": 0.82,
        "descripcion": "Ingeniero ambiental."
    },

    # gen 3: hijos
    {
        "id": "p11", "nombre": "Mateo", "apellido": "Salgado Ríos", "generacion": 3,
        "genero": "M", "ano_nacimiento": 2010, "padres_ids": ["p8", "p9"],
        "inmune_gripe": 0.85, "inmune_covid": 0.80, "inmune_bacteria": 0.88,
        "descripcion": "Estudiante de colegio."
    },
    {
        "id": "p12", "nombre": "Valentina", "apellido": "Salgado Ríos", "generacion": 3,
        "genero": "F", "ano_nacimiento": 2006, "padres_ids": ["p8", "p9"],
        "inmune_gripe": 0.90, "inmune_covid": 0.85, "inmune_bacteria": 0.92,
        "descripcion": "Estudiante universitaria."
    },
    {
        "id": "p14", "nombre": "Diana", "apellido": "Castro Salgado", "generacion": 3,
        "genero": "F", "ano_nacimiento": 2013, "padres_ids": ["p7", "p13"],
        "inmune_gripe": 0.88, "inmune_covid": 0.82, "inmune_bacteria": 0.86,
        "descripcion": "Estudiante de primaria."
    },
    {
        "id": "p16", "nombre": "Sofía", "apellido": "Camacho Gómez", "generacion": 3,
        "genero": "F", "ano_nacimiento": 2018, "padres_ids": ["p10", "p15"],
        "inmune_gripe": 0.84, "inmune_covid": 0.80, "inmune_bacteria": 0.82,
        "descripcion": "Hija menor de la familia."
    },
    {
        "id": "p19", "nombre": "Lucas", "apellido": "Morales Camacho", "generacion": 3,
        "genero": "M", "ano_nacimiento": 2019, "padres_ids": ["p17", "p18"],
        "inmune_gripe": 0.86, "inmune_covid": 0.82, "inmune_bacteria": 0.84,
        "descripcion": "Hijo menor de Mariana y Gabriel."
    },
]

ETIQUETAS_GENERACION = {0: "Bisabuelos", 1: "Abuelos", 2: "Padres", 3: "Hijos"}
