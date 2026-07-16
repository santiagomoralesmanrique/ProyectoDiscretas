"""
arbol.py
--------
Define ArbolGenealogico: la estructura que contiene todos los
Nodo (personas), sabe construirse a partir de una lista de
registros (como si vinieran de una base de datos) y calcula la
posición (x, y) donde debe dibujarse cada nodo.
"""

from nodo import Nodo
import random

NOMBRES_MASCULINOS = [
    "Carlos", "Juan", "Pedro", "Luis", "Mateo", "Andrés", "Alejandro",
    "Santiago", "Sebastián", "Diego", "Manuel", "José", "Francisco",
    "Javier", "Daniel", "David", "Felipe", "Hugo", "Lucas", "Nicolás",
    "Fernando", "Gabriel", "Ricardo"
]

NOMBRES_FEMENINOS = [
    "María", "Ana", "Lucía", "Daniela", "Valentina", "Sofía", "Camila",
    "Gabriela", "Isabella", "Mariana", "Laura", "Andrea", "Elena",
    "Clara", "Paula", "Marta", "Rosario", "Carmen", "Luisa", "Beatriz",
    "Silvia", "Patricia", "Adriana"
]

APELLIDOS = [
    "Camacho", "Núñez", "Salgado", "Ríos", "Fernández", "Duarte", "Medina",
    "Gómez", "Rodríguez", "Sánchez", "Pérez", "López", "González",
    "Martínez", "García", "Ramírez", "Torres", "Díaz", "Vargas", "Castro",
    "Ortiz", "Morales"
]

TEMPLATES_DESCRIPCION = [
    "Nació en una época de grandes cambios. Se dedicó al campo y a la familia.",
    "Estudió en la capital y regresó para aportar al desarrollo de la comunidad.",
    "Apasionado por la música y el arte, siempre alegraba las reuniones familiares.",
    "Emprendedor desde joven, fundó un pequeño negocio local de café.",
    "Una persona amable, recordada por su sabiduría y consejos.",
    "Ingeniero de profesión, le encanta viajar y documentar la historia familiar.",
    "Científico aficionado, siempre buscando entender cómo funciona el mundo.",
    "Gran deportista y amante de la naturaleza, recorrió gran parte del país.",
    "Escritor aficionado, llenaba cuadernos con historias de su juventud.",
    "Se dedicó a la enseñanza y formó a muchas generaciones en su comunidad."
]


class ArbolGenealogico:
    def __init__(self):
        self.nodos = {}  # id -> Nodo   (dict preserva el orden de inserción)

    # -----------------------------------------------------------
    # Construcción
    # -----------------------------------------------------------
    def agregar_persona(self, id_persona, nombre, apellido, descripcion,
                         generacion, padres_ids=None, pareja_id=None,
                         genero="M", año_nacimiento=1980,
                         inmune_gripe=0.5, inmune_covid=0.5, inmune_bacteria=0.5):
        """
        Crea un Nodo nuevo y lo conecta con sus padres / pareja,
        siempre y cuando esos ids ya existan en el árbol.
        Devuelve el Nodo creado.
        """
        if id_persona in self.nodos:
            raise ValueError(f"El id '{id_persona}' ya existe en el árbol")

        nodo = Nodo(id_persona, nombre, apellido, descripcion, generacion,
                    genero=genero, año_nacimiento=año_nacimiento,
                    inmune_gripe=inmune_gripe, inmune_covid=inmune_covid, inmune_bacteria=inmune_bacteria)
        self.nodos[id_persona] = nodo

        for id_padre in (padres_ids or []):
            padre = self.nodos.get(id_padre)
            if padre is not None:
                padre.agregar_hijo(nodo)

        if pareja_id:
            pareja = self.nodos.get(pareja_id)
            if pareja is not None:
                nodo.emparejar_con(pareja)

        return nodo

    def cargar_desde_lista(self, registros):
        """
        Recibe una lista de diccionarios -tal como llegarían de una
        consulta SQL, un archivo JSON o una API- y construye el
        árbol completo. Ver datos_prueba.py para el formato esperado.
        """
        for r in registros:
            self.agregar_persona(
                id_persona=r["id"],
                nombre=r["nombre"],
                apellido=r["apellido"],
                descripcion=r["descripcion"],
                generacion=r["generacion"],
                padres_ids=r.get("padres_ids", []),
                pareja_id=r.get("pareja_id"),
                genero=r.get("genero", "M"),
                año_nacimiento=r.get("año_nacimiento", 1980),
                inmune_gripe=r.get("inmune_gripe", 0.5),
                inmune_covid=r.get("inmune_covid", 0.5),
                inmune_bacteria=r.get("inmune_bacteria", 0.5),
            )

    def quitar_ultima_persona(self):
        """Elimina el último nodo agregado (útil para el botón 'Quitar última')."""
        if not self.nodos:
            return None
        ultimo_id = list(self.nodos.keys())[-1]
        nodo = self.nodos.pop(ultimo_id)
        nodo.desconectar()
        return nodo

    def siguiente_id_disponible(self):
        """Genera un id nuevo tipo 'p13', 'p14', ... para nodos agregados desde la UI."""
        n = len(self.nodos) + 1
        while f"p{n}" in self.nodos:
            n += 1
        return f"p{n}"

    # -----------------------------------------------------------
    # Consultas
    # -----------------------------------------------------------
    def por_generacion(self):
        """{generacion: [Nodo, Nodo, ...]} ordenado de menor a mayor."""
        filas = {}
        for nodo in self.nodos.values():
            filas.setdefault(nodo.generacion, []).append(nodo)
        return dict(sorted(filas.items()))

    def generacion_maxima(self):
        if not self.nodos:
            return 0
        return max(n.generacion for n in self.nodos.values())

    def parejas_unicas(self):
        """Devuelve pares (a, b) sin repetir, para dibujar el enlace conyugal una sola vez."""
        vistos = set()
        resultado = []
        for nodo in self.nodos.values():
            if nodo.pareja is None:
                continue
            clave = frozenset({nodo.id, nodo.pareja.id})
            if clave not in vistos:
                vistos.add(clave)
                resultado.append((nodo, nodo.pareja))
        return resultado

    # -----------------------------------------------------------
    # Layout (posiciones para dibujar)
    # -----------------------------------------------------------
    def calcular_posiciones(self, ancho_lienzo, margen_x=80, y_inicial=80, alto_fila=170):
        """
        Una fila por generación (0 arriba, generaciones más nuevas
        hacia abajo). Dentro de cada fila, los nodos se reparten
        uniformemente a lo ancho del lienzo.
        """
        for generacion, personas in self.por_generacion().items():
            n = len(personas)
            usable = ancho_lienzo - margen_x * 2
            for i, persona in enumerate(personas):
                persona.x = margen_x + (i + 0.5) * (usable / n)
                persona.y = y_inicial + generacion * alto_fila

    def punto_union_padres(self, nodo):
        """Punto medio entre los padres de `nodo`: de ahí sale la rama hacia él."""
        if not nodo.padres:
            return None
        x = sum(p.x for p in nodo.padres) / len(nodo.padres)
        y = sum(p.y for p in nodo.padres) / len(nodo.padres)
        return x, y

    # -----------------------------------------------------------
    # Algoritmos de Matemáticas Discretas (Grafos)
    # -----------------------------------------------------------
    def es_dag(self):
        """Verifica si el grafo dirigido es acíclico (DAG) usando DFS con coloreado."""
        visitados = {n_id: 0 for n_id in self.nodos} # 0=blanco, 1=gris, 2=negro

        def dfs_tiene_ciclo(nodo_id):
            visitados[nodo_id] = 1 # gris (en proceso)
            nodo = self.nodos[nodo_id]
            for hijo in nodo.hijos:
                if visitados[hijo.id] == 1:
                    return True # ciclo detectado (arista de retroceso)
                elif visitados[hijo.id] == 0:
                    if dfs_tiene_ciclo(hijo.id):
                        return True
            visitados[nodo_id] = 2 # negro (completado)
            return False

        for n_id in self.nodos:
            if visitados[n_id] == 0:
                if dfs_tiene_ciclo(n_id):
                    return False
        return True

    def es_conexo(self):
        """Determina si la red familiar está completamente conectada (grafo no dirigido)."""
        if not self.nodos:
            return True
        inicio_id = list(self.nodos.keys())[0]
        visitados = {inicio_id}
        cola = [inicio_id]

        while cola:
            actual_id = cola.pop(0)
            nodo = self.nodos[actual_id]
            vecinos = [p.id for p in nodo.padres] + [h.id for h in nodo.hijos]
            if nodo.pareja:
                vecinos.append(nodo.pareja.id)

            for v_id in vecinos:
                if v_id not in visitados:
                    visitados.add(v_id)
                    cola.append(v_id)

        return len(visitados) == len(self.nodos)

    def obtener_componentes_conexas(self):
        """Calcula el número de componentes conexas (familias aisladas)."""
        visitados = set()
        componentes = 0

        for nodo_id in self.nodos:
            if nodo_id not in visitados:
                componentes += 1
                cola = [nodo_id]
                visitados.add(nodo_id)
                while cola:
                    actual_id = cola.pop(0)
                    nodo = self.nodos[actual_id]
                    vecinos = [p.id for p in nodo.padres] + [h.id for h in nodo.hijos]
                    if nodo.pareja:
                        vecinos.append(nodo.pareja.id)
                    for v_id in vecinos:
                        if v_id not in visitados:
                            visitados.add(v_id)
                            cola.append(v_id)
        return componentes

    def obtener_grados(self):
        """Calcula los grados de cada nodo (padres=in, hijos=out, pareja, total)."""
        grados = {}
        for n_id, nodo in self.nodos.items():
            in_deg = len(nodo.padres)
            out_deg = len(nodo.hijos)
            pareja_deg = 1 if nodo.pareja else 0
            total_deg = in_deg + out_deg + pareja_deg
            grados[n_id] = {
                'in': in_deg,
                'out': out_deg,
                'pareja': pareja_deg,
                'total': total_deg
            }
        return grados

    def buscar_camino_parentesco(self, id_a, id_b):
        """Encuentra el camino más corto entre dos nodos (BFS) y su parentesco."""
        if id_a not in self.nodos or id_b not in self.nodos:
            return None, "Uno o ambos nodos no existen."
        if id_a == id_b:
            return [id_a], "Es la misma persona."

        cola = [[id_a]]
        visitados = {id_a}

        camino = None
        while cola:
            ruta = cola.pop(0)
            ultimo = ruta[-1]
            if ultimo == id_b:
                camino = ruta
                break

            nodo = self.nodos[ultimo]
            vecinos = [p.id for p in nodo.padres] + [h.id for h in nodo.hijos]
            if nodo.pareja:
                vecinos.append(nodo.pareja.id)

            for v_id in vecinos:
                if v_id not in visitados:
                    visitados.add(v_id)
                    cola.append(ruta + [v_id])

        if not camino:
            return None, "No existe una relación o camino que conecte a estas personas."

        return camino, self.traducir_camino(camino)

    def obtener_tipo_paso(self, n1, n2):
        if n2 in n1.padres:
            return "UP"
        if n2 in n1.hijos:
            return "DOWN"
        if n1.pareja == n2:
            return "SPOUSE"
        return "UNKNOWN"

    def traducir_camino(self, camino):
        """Traduce un camino de nodos a una relación familiar en español."""
        nodos_ruta = [self.nodos[nid] for nid in camino]
        pasos = []
        for i in range(len(nodos_ruta) - 1):
            pasos.append(self.obtener_tipo_paso(nodos_ruta[i], nodos_ruta[i+1]))

        pasos_tupla = tuple(pasos)

        diccionario_relaciones = {
            ("UP",): "Padre/Madre",
            ("DOWN",): "Hijo/a",
            ("SPOUSE",): "Pareja",
            ("UP", "UP"): "Abuelo/a",
            ("DOWN", "DOWN"): "Nieto/a",
            ("UP", "DOWN"): "Hermano/a",
            ("SPOUSE", "DOWN"): "Hijastro/a",
            ("UP", "SPOUSE"): "Padrastro/Madrastra",
            ("DOWN", "SPOUSE"): "Yerno/Nuera",
            ("SPOUSE", "UP"): "Suegro/a",
            ("UP", "UP", "UP"): "Bisabuelo/a",
            ("DOWN", "DOWN", "DOWN"): "Biznieto/a",
            ("UP", "UP", "DOWN"): "Tío/a",
            ("UP", "DOWN", "DOWN"): "Sobrino/a",
            ("UP", "DOWN", "SPOUSE"): "Cuñado/a",
            ("SPOUSE", "UP", "DOWN"): "Cuñado/a",
            ("UP", "UP", "DOWN", "DOWN"): "Primo/a hermano/a",
            ("UP", "UP", "UP", "DOWN"): "Tío/a abuelo/a",
            ("UP", "DOWN", "DOWN", "DOWN"): "Sobrino/a nieto/a",
        }

        if pasos_tupla in diccionario_relaciones:
            return diccionario_relaciones[pasos_tupla]

        # Fallback descriptivo paso a paso
        descripcion_pasos = []
        for i in range(len(nodos_ruta) - 1):
            n_act = nodos_ruta[i]
            n_sig = nodos_ruta[i+1]
            tipo = self.obtener_tipo_paso(n_act, n_sig)

            if tipo == "UP":
                rel = "es progenitor/a de"
            elif tipo == "DOWN":
                rel = "es hijo/a de"
            elif tipo == "SPOUSE":
                rel = "es pareja de"
            else:
                rel = "se conecta con"

            descripcion_pasos.append(f"{n_sig.nombre} ({rel} {n_act.nombre})")

        return " -> ".join(descripcion_pasos)

    def encontrar_camino_hamiltoniano(self):
        """Encuentra un camino hamiltoniano en el grafo no dirigido (backtracking)."""
        n_ids = list(self.nodos.keys())
        n = len(n_ids)
        if n <= 1:
            return n_ids

        def backtrack(path, visited):
            if len(path) == n:
                return path

            ultimo = path[-1]
            nodo = self.nodos[ultimo]
            vecinos = [p.id for p in nodo.padres] + [h.id for h in nodo.hijos]
            if nodo.pareja:
                vecinos.append(nodo.pareja.id)

            for v in vecinos:
                if v not in visited:
                    visited.add(v)
                    res = backtrack(path + [v], visited)
                    if res:
                        return res
                    visited.remove(v)
            return None

        for inicio in n_ids:
            res = backtrack([inicio], {inicio})
            if res:
                return res
        return None

    def analizar_propiedades_discretas(self):
        """Realiza un análisis completo de teoría de grafos del árbol."""
        grados = self.obtener_grados()
        total_nodos = len(self.nodos)

        if total_nodos == 0:
            return {
                "nodos": 0, "aristas": 0, "conexo": True, "dag": True,
                "max_grado": 0, "max_grado_nombre": "N/A",
                "euleriano": False, "hamiltoniano": False, "explicacion": "El grafo está vacío."
            }

        # Cantidad de aristas dirigidas (padre -> hijo)
        aristas = sum(len(n.hijos) for n in self.nodos.values())

        # Grado máximo
        max_id = max(grados.keys(), key=lambda k: grados[k]['total'])
        max_val = grados[max_id]['total']
        max_nombre = self.nodos[max_id].nombre_completo()

        # Conectividad
        conexo = self.es_conexo()

        # Detección de ciclos
        dag = self.es_dag()

        # Eulerian Path en grafo no dirigido
        # Todos los vértices impares deben ser 0 o 2.
        impares = sum(1 for k in grados.values() if k['total'] % 2 != 0)
        euleriano = conexo and (impares == 0 or impares == 2)

        # Hamiltonian Path
        hamiltoniano_ruta = self.encontrar_camino_hamiltoniano()
        hamiltoniano = hamiltoniano_ruta is not None

        return {
            "nodos": total_nodos,
            "aristas": aristas,
            "conexo": conexo,
            "dag": dag,
            "max_grado": max_val,
            "max_grado_nombre": max_nombre,
            "euleriano": euleriano,
            "hamiltoniano": hamiltoniano,
            "ruta_hamiltoniana": hamiltoniano_ruta
        }

    # -----------------------------------------------------------
    # Algoritmos de Simulación de Propagación
    # -----------------------------------------------------------
    def simular_propagacion_apellido(self, id_origen):
        """Propaga el primer apellido de origen a sus descendientes usando BFS."""
        for nodo in self.nodos.values():
            nodo.estado_simulado = None

        if id_origen not in self.nodos:
            return []

        origen = self.nodos[id_origen]
        apellido_a_propagar = origen.apellido.split()[0] # primer apellido

        pasos = [[origen.id]]
        origen.estado_simulado = f"Ape: {apellido_a_propagar}"

        cola = [origen]
        visitados = {origen.id}

        while cola:
            ronda = []
            nivel_actual = len(cola)
            for _ in range(nivel_actual):
                actual = cola.pop(0)
                # Sólo se propaga a los hijos (descendientes directos)
                for hijo in actual.hijos:
                    if hijo.id not in visitados:
                        # En la cultura hispana, heredan el apellido si es transmitido
                        hijo.estado_simulado = f"Ape: {apellido_a_propagar}"
                        ronda.append(hijo.id)
                        visitados.add(hijo.id)
                        cola.append(hijo)
            if ronda:
                pasos.append(ronda)

        return pasos

    def calcular_prob_contagio(self, receptor, prob_base, tipo_enfermedad):
        """
        Calcula la probabilidad final de contagio para un receptor concreto
        según el tipo de enfermedad y la inmunidad respectiva de esa persona.
        """
        if tipo_enfermedad == "gripe":
            inmunidad = receptor.inmune_gripe
        elif tipo_enfermedad == "covid":
            inmunidad = receptor.inmune_covid
        elif tipo_enfermedad == "bacteria":
            inmunidad = receptor.inmune_bacteria
        else:
            inmunidad = 0.5
            
        factor_inmune = 1.0 - inmunidad  # 0 = inmune total, 1 = sin defensa
        prob_final = prob_base * factor_inmune
        return min(max(prob_final, 0.0), 1.0)

    def simular_propagacion_contagio(self, id_origen, prob_base, tipo_enfermedad="gripe"):
        """
        Propaga un contagio por la red familiar usando BFS con probabilidad
        de infección PERSONALIZADA según el tipo de enfermedad y la inmunidad correspondiente.
        """
        for nodo in self.nodos.values():
            nodo.estado_simulado = "sano"

        if id_origen not in self.nodos:
            return []

        origen = self.nodos[id_origen]
        origen.estado_simulado = "infectado"

        pasos = [[origen.id]]
        infectados_actuales = [origen]
        visitados = {origen.id}

        for _ in range(12):  # límite de rondas para evitar bucles infinitos
            ronda = []
            for inf in infectados_actuales:
                vecinos = inf.padres + inf.hijos
                if inf.pareja:
                    vecinos.append(inf.pareja)

                for v in vecinos:
                    if v.id not in visitados:
                        prob_v = self.calcular_prob_contagio(v, prob_base, tipo_enfermedad)
                        if random.random() < prob_v:
                            v.estado_simulado = "infectado"
                            ronda.append(v.id)
                            visitados.add(v.id)
            if not ronda:
                break
            pasos.append(ronda)
            infectados_actuales = [self.nodos[nid] for nid in ronda]

        return pasos

    def simular_propagacion_genetica(self, id_origen):
        """Simula la herencia mendeliana de un gen mutado (A) desde el origen."""
        # Todos los nodos inician con genotipo sano 'aa'
        for nodo in self.nodos.values():
            nodo.estado_simulado = "aa"

        if id_origen not in self.nodos:
            return []

        origen = self.nodos[id_origen]
        origen.estado_simulado = "Aa" # Portador original

        pasos = [[origen.id]]

        # Ordenar nodos por generación para procesar padres antes que hijos
        nodos_ordenados = sorted(self.nodos.values(), key=lambda n: n.generacion)
        gen_origen = origen.generacion

        modificados = []
        for nodo in nodos_ordenados:
            if nodo.id == origen.id or nodo.generacion <= gen_origen:
                continue

            if nodo.padres:
                alelos_heredados = []
                for padre in nodo.padres:
                    genotipo_padre = padre.estado_simulado or "aa"
                    # Seleccionar un alelo al azar del padre/madre
                    alelos_heredados.append(random.choice(list(genotipo_padre)))

                # Si sólo hay un padre registrado en el árbol, el otro alelo es por defecto 'a'
                if len(alelos_heredados) == 1:
                    alelos_heredados.append("a")

                alelos_heredados.sort()
                genotipo_hijo = "".join(alelos_heredados)
                # Normalizar a 'Aa' en lugar de 'aA'
                if genotipo_hijo == "aA":
                    genotipo_hijo = "Aa"

                nodo.estado_simulado = genotipo_hijo
                if genotipo_hijo != "aa":
                    modificados.append(nodo.id)

        if modificados:
            # Agrupar modificados por generación para la animación por capas
            filas_modificados = {}
            for nid in modificados:
                n = self.nodos[nid]
                filas_modificados.setdefault(n.generacion, []).append(nid)

            for gen in sorted(filas_modificados.keys()):
                pasos.append(filas_modificados[gen])

        return pasos

    def generar_arbol_aleatorio(self, X, H):
        """
        Genera un árbol genealógico aleatorio con X personas y H generaciones (pisos).
        Aplica restricciones estrictas:
          - X >= 2H - 1 (mínimo 2 personas por piso para formar parejas con descendencia, 1 en el último)
          - Parejas heterosexuales y acopladas formalmente para tener hijos.
          - Mínima diferencia de año de nacimiento de 17 años entre padres e hijos.
          - Ningún hijo puede tener un padre soltero (tienen exactamente 2 padres en el árbol).
        """
        if X < 2 * H - 1:
            raise ValueError(f"No es posible armar un árbol de {H} pisos con {X} personas bajo las restricciones familiares.\nSe requiere al menos 2 personas por piso para tener descendencia (y 1 en el último), total mínimo: {2 * H - 1} personas.")

        self.nodos.clear()

        # Distribuir las X personas en H generaciones.
        # Las primeras H-1 generaciones deben tener al menos 2 personas para poder formar parejas con hijos.
        personas_por_gen = [2] * (H - 1) + [1] if H > 1 else [1]
        
        # Distribuir los restantes aleatoriamente
        restantes = X - sum(personas_por_gen)
        for _ in range(restantes):
            gen_elegida = random.randint(0, H - 1)
            personas_por_gen[gen_elegida] += 1

        # Listas de personas creadas por generación
        nodos_por_gen = [[] for _ in range(H)]

        # Determinar el año de inicio adaptativo para que no exceda 2026
        # Si H es grande, empezamos en el pasado más lejano (hasta 1840)
        año_inicio = max(1840, 2020 - (H * 18))

        # Generar personas para la generación 0 (los más antiguos)
        # Dividimos en masculino y femenino de forma equitativa
        num_f0 = personas_por_gen[0] // 2
        num_m0 = personas_por_gen[0] - num_f0
        generos_gen0 = ["F"] * num_f0 + ["M"] * num_m0
        random.shuffle(generos_gen0)

        for i in range(personas_por_gen[0]):
            genero = generos_gen0[i]
            nombre = random.choice(NOMBRES_MASCULINOS if genero == "M" else NOMBRES_FEMENINOS)
            ape1 = random.choice(APELLIDOS)
            ape2 = random.choice(APELLIDOS)
            while ape2 == ape1:
                ape2 = random.choice(APELLIDOS)
            apellido = f"{ape1} {ape2}"
            
            # Año de nacimiento: alrededor del año_inicio
            año_nacimiento = año_inicio + random.randint(-5, 5)
            
            # Inmunidades específicas
            inmune_gripe = round(random.uniform(0.1, 0.4), 2)
            inmune_covid = round(random.uniform(0.1, 0.4), 2)
            inmune_bacteria = round(random.uniform(0.1, 0.4), 2)
            
            id_persona = f"p{len(self.nodos) + 1}"
            desc = random.choice(TEMPLATES_DESCRIPCION)
            
            nodo = self.agregar_persona(
                id_persona=id_persona,
                nombre=nombre,
                apellido=apellido,
                descripcion=desc,
                generacion=0,
                genero=genero,
                año_nacimiento=año_nacimiento,
                inmune_gripe=inmune_gripe,
                inmune_covid=inmune_covid,
                inmune_bacteria=inmune_bacteria
            )
            nodos_por_gen[0].append(nodo)

        # Función auxiliar para emparejar heterosexuales de una generación
        def emparejar_gen_hetero(g_idx):
            nodos = nodos_por_gen[g_idx]
            mujeres = [n for n in nodos if n.genero == "F"]
            hombres = [n for n in nodos if n.genero == "M"]
            random.shuffle(mujeres)
            random.shuffle(hombres)
            
            parejas = []
            while mujeres and hombres:
                m = mujeres.pop()
                # Buscar un hombre que no sea su hermano (si comparten padres)
                h_idx = -1
                for idx, h in enumerate(hombres):
                    comparten_padres = set(m.padres) & set(h.padres) if (m.padres and h.padres) else False
                    if not comparten_padres:
                        h_idx = idx
                        break
                
                if h_idx != -1:
                    h = hombres.pop(h_idx)
                else:
                    h = hombres.pop()
                    
                m.emparejar_con(h)
                parejas.append((m, h))
            return parejas

        # Parejas de generación 0
        parejas_por_gen = [[] for _ in range(H)]
        parejas_por_gen[0] = emparejar_gen_hetero(0)

        # Generar generaciones 1 a H-1
        for g in range(1, H):
            # Para heredar, usamos solo las parejas de la generación anterior como unidades de padres
            padres_parejas = list(parejas_por_gen[g-1])
            
            num_hijos = personas_por_gen[g]
            
            # Si g < H-1, queremos asegurar que haya al menos 1 hombre y 1 mujer
            # para que puedan formar parejas en esta generación.
            generos_gen = []
            if g < H - 1 and num_hijos >= 2:
                num_fg = num_hijos // 2
                num_mg = num_hijos - num_fg
                generos_gen = ["F"] * num_fg + ["M"] * num_mg
                random.shuffle(generos_gen)
            else:
                generos_gen = [random.choice(["M", "F"]) for _ in range(num_hijos)]

            # Asignar cada hijo a una pareja de padres
            asignacion_padres = []
            if len(padres_parejas) <= num_hijos:
                # Cada pareja tiene al menos un hijo
                for cp in padres_parejas:
                    asignacion_padres.append(cp)
                # El resto de hijos se asignan al azar
                for _ in range(num_hijos - len(padres_parejas)):
                    asignacion_padres.append(random.choice(padres_parejas))
            else:
                # Más parejas que hijos, asignamos hijos a parejas distintas
                random.shuffle(padres_parejas)
                for i in range(num_hijos):
                    asignacion_padres.append(padres_parejas[i])

            # Crear hijos
            for idx_hijo in range(num_hijos):
                madr, padr = asignacion_padres[idx_hijo]
                padres_ids = [madr.id, padr.id]
                
                # Combinación de apellidos
                ape_madr = madr.apellido.split()[0]
                ape_padr = padr.apellido.split()[0]
                # En español, usualmente primer apellido del padre y primer apellido de la madre
                # pero los tomamos de forma mezclada
                apellido = f"{ape_padr} {ape_madr}"
                
                genero = generos_gen[idx_hijo]
                nombre = random.choice(NOMBRES_MASCULINOS if genero == "M" else NOMBRES_FEMENINOS)
                
                # Año nacimiento coherente: al menos 17 años menor que el menor de los padres
                año_padre_max = max(madr.año_nacimiento, padr.año_nacimiento)
                año_nacimiento = año_padre_max + random.randint(17, 21)
                
                # Inmunidad específica
                inmune_gripe = round(random.uniform(0.3, 0.9), 2)
                inmune_covid = round(random.uniform(0.3, 0.9), 2)
                inmune_bacteria = round(random.uniform(0.3, 0.9), 2)
                
                id_persona = f"p{len(self.nodos) + 1}"
                desc = random.choice(TEMPLATES_DESCRIPCION)

                nodo = self.agregar_persona(
                    id_persona=id_persona,
                    nombre=nombre,
                    apellido=apellido,
                    descripcion=desc,
                    generacion=g,
                    padres_ids=padres_ids,
                    genero=genero,
                    año_nacimiento=año_nacimiento,
                    inmune_gripe=inmune_gripe,
                    inmune_covid=inmune_covid,
                    inmune_bacteria=inmune_bacteria
                )
                nodos_por_gen[g].append(nodo)

            parejas_por_gen[g] = emparejar_gen_hetero(g)

    def simular_propagacion_multifactorial(self, id_origen):
        """
        Simula la propagación de una enfermedad hereditaria multifactorial.
        La probabilidad de heredar disminuye a la mitad con cada nivel generacional
        de distancia desde el origen de la mutación.
        P = 0.8 * (0.5 ** (generacion_hijo - generacion_origen))
        """
        for nodo in self.nodos.values():
            nodo.estado_simulado = "sano"

        if id_origen not in self.nodos:
            return []

        origen = self.nodos[id_origen]
        origen.estado_simulado = "infectado"

        pasos = [[origen.id]]

        # Ordenar nodos por generación para procesar de arriba a abajo
        nodos_ordenados = sorted(self.nodos.values(), key=lambda n: n.generacion)
        gen_origen = origen.generacion

        modificados = []
        for nodo in nodos_ordenados:
            if nodo.id == origen.id or nodo.generacion <= gen_origen:
                continue

            # Para heredar, alguno de sus padres en el árbol debe estar infectado
            padres_infectados = [p for p in nodo.padres if p.estado_simulado == "infectado"]
            if padres_infectados:
                # Distancia generacional
                distancia = nodo.generacion - gen_origen
                prob_herencia = 0.8 * (0.5 ** distancia)
                if random.random() < prob_herencia:
                    nodo.estado_simulado = "infectado"
                    modificados.append(nodo.id)

        if modificados:
            # Agrupar modificados por generación para la animación por capas
            filas_modificados = {}
            for nid in modificados:
                n = self.nodos[nid]
                filas_modificados.setdefault(n.generacion, []).append(nid)

            for gen in sorted(filas_modificados.keys()):
                pasos.append(filas_modificados[gen])

        return pasos


