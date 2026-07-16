"""
nodo.py
-------
Define la clase Nodo: la unidad básica del árbol genealógico.
Cada Nodo representa UNA persona y sabe quiénes son sus padres,
su pareja y sus hijos, así que el árbol completo es, en el fondo,
una red de objetos Nodo conectados entre sí.
"""


class Nodo:
    """Una persona dentro del árbol genealógico."""

    def __init__(self, id_persona, nombre, apellido, descripcion, generacion,
                 genero="M", año_nacimiento=1980,
                 inmune_gripe=0.5, inmune_covid=0.5, inmune_bacteria=0.5):
        # --- datos que vienen de la "base de datos" ---
        self.id = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.descripcion = descripcion
        self.generacion = generacion  # 0 = generación más antigua del árbol
        self.genero = genero          # 'M' o 'F'
        self.año_nacimiento = año_nacimiento

        # --- atributos de salud (influyen en la probabilidad de contagio) ---
        self.inmune_gripe = inmune_gripe
        self.inmune_covid = inmune_covid
        self.inmune_bacteria = inmune_bacteria

        # --- relaciones con otros nodos ---
        self.padres = []      # 0, 1 o 2 objetos Nodo (exactamente 2 si se especifican)
        self.hijos = []       # lista de objetos Nodo
        self.pareja = None    # objeto Nodo o None

        # --- posición calculada por ArbolGenealogico para dibujar ---
        self.x = 0
        self.y = 0

        # --- estados para visualización de caminos y simulaciones ---
        self.resaltado = False
        self.estado_simulado = None  # None, 'infectado', 'sano', 'portador', etc.

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def agregar_hijo(self, nodo_hijo):
        """Conecta este nodo como padre/madre de nodo_hijo (en ambos sentidos)."""
        if nodo_hijo not in self.hijos:
            self.hijos.append(nodo_hijo)
        if self not in nodo_hijo.padres:
            nodo_hijo.padres.append(self)

    def emparejar_con(self, otro_nodo):
        """Marca a dos nodos como pareja (en ambos sentidos)."""
        self.pareja = otro_nodo
        otro_nodo.pareja = self

    def desconectar(self):
        """Elimina todas las referencias hacia este nodo desde sus padres y pareja."""
        for padre in self.padres:
            if self in padre.hijos:
                padre.hijos.remove(self)
        if self.pareja is not None:
            self.pareja.pareja = None
            self.pareja = None

    def __repr__(self):
        return f"Nodo({self.nombre_completo()!r}, generacion={self.generacion})"
