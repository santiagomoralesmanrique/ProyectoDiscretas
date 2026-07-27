# nodo.py - clase bsica para representar una persona en el arbol

class Nodo:
    def __init__(self, id_persona, nombre, apellido, descripcion, generacion,
                 genero="M", ano_nacimiento=1980,
                 inmune_gripe=0.5, inmune_covid=0.5, inmune_bacteria=0.5, **kwargs):
        # datos de la persona
        self.id = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.descripcion = descripcion
        self.generacion = generacion  # 0 es la mas vieja
        self.genero = genero          # M o F
        
        # permite recibir ano_nacimiento o año_nacimiento por keyword arg
        ano = kwargs.get("año_nacimiento", ano_nacimiento)
        self.ano_nacimiento = ano
        self.año_nacimiento = ano

        # probabilidades de salud / inmunidad
        self.inmune_gripe = inmune_gripe
        self.inmune_covid = inmune_covid
        self.inmune_bacteria = inmune_bacteria

        # relaciones del grafo
        self.padres = []      # lista con los papas (max 2)
        self.hijos = []       # lista de hijos
        self.pareja = None    # nodo pareja o None

        # pos para el dibujo en el canvas
        self.x = 0
        self.y = 0

        # flags de estado visual
        self.resaltado = False
        self.estado_simulado = None  # infectado, sano, etc

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def agregar_hijo(self, nodo_hijo):
        if nodo_hijo not in self.hijos:
            self.hijos.append(nodo_hijo)
        if self not in nodo_hijo.padres:
            nodo_hijo.padres.append(self)

    def emparejar_con(self, otro_nodo):
        self.pareja = otro_nodo
        otro_nodo.pareja = self

    def desconectar(self):
        for p in self.padres:
            if self in p.hijos:
                p.hijos.remove(self)
        if self.pareja is not None:
            self.pareja.pareja = None
            self.pareja = None

    def __repr__(self):
        return f"Nodo({self.nombre_completo()!r}, gen={self.generacion})"
