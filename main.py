"""
main.py
-------
Interfaz gráfica (Tkinter) que dibuja el árbol genealógico y anima
su construcción generación por generación, de arriba (los más
antiguos) hacia abajo. Ejecútalo con:

    python main.py

Controles:
    - Reiniciar animación : vuelve a reproducir la construcción del árbol.
    - Agregar persona      : abre un formulario para crear un Nodo nuevo
                              y conectarlo con sus padres / pareja.
    - Quitar última        : elimina el último Nodo agregado.
    - Clic en una tarjeta   : muestra la ficha completa de esa persona.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from arbol import ArbolGenealogico
import datos_prueba

# ---------------------------------------------------------------
# Paleta y tipografías (si tu sistema no tiene estas fuentes,
# Tkinter las sustituye automáticamente por una equivalente)
# ---------------------------------------------------------------
COLOR_FONDO = "#12201A"
COLOR_PAPEL = "#EFE6CC"
COLOR_PAPEL_OSCURO = "#E4D8B4"
COLOR_TINTA = "#2B2118"
COLOR_TINTA_SUAVE = "#5A4C36"
COLOR_ORO = "#C9A227"
COLOR_RAMA = "#8A6A45"
COLOR_MUSGO = "#6E8F6A"
COLOR_BOTON = "#1C2A21"
COLOR_BOTON_TEXTO = "#E4C766"

FUENTE_DISPLAY = "Georgia"
FUENTE_CUERPO = "Verdana"
FUENTE_MONO = "Consolas"

ANCHO_TARJETA = 145
ALTO_TARJETA = 95


def curva_bezier(p0, p1, p2, p3, num_puntos=16):
    """Devuelve num_puntos puntos (x, y) a lo largo de una curva de Bézier cúbica."""
    puntos = []
    for i in range(num_puntos + 1):
        t = i / num_puntos
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        puntos.append((x, y))
    return puntos


class VentanaArbol(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol Genealógico — proyecto de nodos")
        self.configure(bg=COLOR_FONDO)
        self.geometry("1420x780")
        self.minsize(1000, 520)

        self.arbol = ArbolGenealogico()
        self.arbol.cargar_desde_lista(datos_prueba.PERSONAS_DE_PRUEBA)

        self._despues_ids = []       # ids de after() pendientes, para poder cancelarlos
        self._cache_puntos_rama = {}  # puntos precalculados de cada curva mientras se dibuja

        # Variables para controles del panel lateral
        self.var_persona_a = tk.StringVar()
        self.var_persona_b = tk.StringVar()
        self.var_sim_tipo = tk.StringVar(value="Apellido")
        self.var_sim_origen = tk.StringVar()
        self.var_sim_prob = tk.DoubleVar(value=0.5)

        self._construir_interfaz()
        self._actualizar_opciones_sidebar()
        self.after(200, self.reiniciar_animacion)

    # -----------------------------------------------------------
    # Construcción de la interfaz
    # -----------------------------------------------------------
    def _construir_interfaz(self):
        barra = tk.Frame(self, bg=COLOR_FONDO)
        barra.pack(side="top", fill="x", padx=14, pady=(14, 6))

        tk.Label(barra, text="ÁRBOL GENEALÓGICO · FAMILIA CAMACHO NÚÑEZ",
                 bg=COLOR_FONDO, fg=COLOR_PAPEL,
                 font=(FUENTE_DISPLAY, 16, "bold")).pack(side="left")

        botones = tk.Frame(barra, bg=COLOR_FONDO)
        botones.pack(side="right")
        self._boton(botones, "↻  Reiniciar animación", self.reiniciar_animacion).pack(side="left", padx=4)
        self._boton(botones, "➕  Agregar persona", self.abrir_dialogo_agregar).pack(side="left", padx=4)
        self._boton(botones, "🎲  Generar Aleatorio", self.abrir_dialogo_generar_aleatorio).pack(side="left", padx=4)
        self._boton(botones, "🗑  Quitar última", self.quitar_ultima).pack(side="left", padx=4)

        tk.Label(self, text="Datos de prueba — clic en una tarjeta para ver la ficha completa.",
                 bg=COLOR_FONDO, fg=COLOR_MUSGO, font=(FUENTE_MONO, 9)
                 ).pack(side="top", anchor="w", padx=16, pady=(0, 8))

        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=0)
        contenedor.columnconfigure(2, weight=0)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
        style.configure("TNotebook.Tab", background=COLOR_BOTON, foreground=COLOR_BOTON_TEXTO,
                         font=(FUENTE_MONO, 9), padding=(14, 6))
        style.map("TNotebook.Tab", background=[("selected", COLOR_ORO)],
                  foreground=[("selected", COLOR_TINTA)])

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")
        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestaña)

        # --- Pestaña 1: árbol genealógico ---
        tab_arbol = tk.Frame(self.notebook, bg=COLOR_FONDO)
        tab_arbol.rowconfigure(0, weight=1)
        tab_arbol.columnconfigure(0, weight=1)
        self.notebook.add(tab_arbol, text="  Árbol Genealógico  ")

        self.canvas = tk.Canvas(tab_arbol, bg=COLOR_FONDO, highlightthickness=0)
        vbar = tk.Scrollbar(tab_arbol, orient="vertical", command=self.canvas.yview)
        hbar = tk.Scrollbar(tab_arbol, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="ew")

        # --- Pestaña 2: vista de grafo abstracto ---
        tab_grafo = tk.Frame(self.notebook, bg=COLOR_FONDO)
        tab_grafo.rowconfigure(0, weight=1)
        tab_grafo.columnconfigure(0, weight=1)
        self.notebook.add(tab_grafo, text="   Vista de Grafo  ")

        self.canvas_grafo = tk.Canvas(tab_grafo, bg=COLOR_FONDO, highlightthickness=0)
        vbar_g = tk.Scrollbar(tab_grafo, orient="vertical", command=self.canvas_grafo.yview)
        hbar_g = tk.Scrollbar(tab_grafo, orient="horizontal", command=self.canvas_grafo.xview)
        self.canvas_grafo.configure(yscrollcommand=vbar_g.set, xscrollcommand=hbar_g.set)
        self.canvas_grafo.grid(row=0, column=0, sticky="nsew")
        vbar_g.grid(row=0, column=1, sticky="ns")
        hbar_g.grid(row=1, column=0, sticky="ew")

        # --- PANEL LATERAL DE CONTROL (Con Scroll) ---
        self.sidebar_container = tk.Frame(contenedor, bg=COLOR_FONDO, width=320)
        self.sidebar_container.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(16, 0))
        self.sidebar_container.grid_propagate(False)
        self.sidebar_container.rowconfigure(0, weight=1)
        self.sidebar_container.columnconfigure(0, weight=1)

        self.sidebar_canvas = tk.Canvas(self.sidebar_container, bg=COLOR_FONDO, highlightthickness=0)
        self.sidebar_vbar = tk.Scrollbar(self.sidebar_container, orient="vertical", command=self.sidebar_canvas.yview)
        self.sidebar_canvas.configure(yscrollcommand=self.sidebar_vbar.set)
        
        self.sidebar = tk.Frame(self.sidebar_canvas, bg=COLOR_FONDO)
        self.sidebar_window = self.sidebar_canvas.create_window((0, 0), window=self.sidebar, anchor="nw")
        
        self.sidebar.bind("<Configure>", lambda e: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all")))
        self.sidebar_canvas.bind("<Configure>", lambda e: self.sidebar_canvas.itemconfig(self.sidebar_window, width=e.width))

        self.sidebar_canvas.grid(row=0, column=0, sticky="nsew")
        self.sidebar_vbar.grid(row=0, column=1, sticky="ns")

        def _on_mousewheel(event):
            self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        self.sidebar_canvas.bind("<Enter>", lambda e: self.sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.sidebar_canvas.bind("<Leave>", lambda e: self.sidebar_canvas.unbind_all("<MouseWheel>"))

        # Título del panel lateral
        tk.Label(self.sidebar, text="ANÁLISIS Y SIMULACIÓN", bg=COLOR_FONDO, fg=COLOR_ORO,
                 font=(FUENTE_DISPLAY, 12, "bold")).pack(fill="x", pady=(0, 10))

        # SECCIÓN 1: Identificador de Grafo
        lf_analisis = tk.LabelFrame(self.sidebar, text="  Teoría de Grafos  ", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                     font=(FUENTE_DISPLAY, 10, "bold"), bd=1, relief="solid")
        lf_analisis.pack(fill="x", pady=6, ipady=4)
        
        self.lbl_nodos_edges = tk.Label(lf_analisis, text="Nodos: --  |  Aristas: --", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                         font=(FUENTE_CUERPO, 8))
        self.lbl_nodos_edges.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_dag_conexo = tk.Label(lf_analisis, text="¿Es DAG (sin ciclos)? --\n¿Conexo? --", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                       font=(FUENTE_CUERPO, 8), justify="left")
        self.lbl_dag_conexo.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_euler_hamilton = tk.Label(lf_analisis, text="Haz clic en calcular para ver\nlas propiedades discretas.", bg=COLOR_FONDO, fg=COLOR_PAPEL_OSCURO,
                                            font=(FUENTE_CUERPO, 8), justify="left", wraplength=290)
        self.lbl_euler_hamilton.pack(anchor="w", padx=10, pady=2)
        
        f_botones_analisis = tk.Frame(lf_analisis, bg=COLOR_FONDO)
        f_botones_analisis.pack(fill="x", padx=10, pady=4)
        self._boton_chico(f_botones_analisis, "🧮  Ver Matriz", self.abrir_dialogo_matriz).pack(side="left")
        self._boton_chico(f_botones_analisis, "📊  Calcular Propiedades", self.ejecutar_analisis).pack(side="right")
    
        tk.Label(lf_analisis, text="Colores en 'Vista de Grafo':", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                 font=(FUENTE_CUERPO, 8, "bold")).pack(anchor="w", padx=10, pady=(6, 2))
        self._fila_leyenda_color(lf_analisis, "#C0392B", "Rojo = persona con grado impar")
        self._fila_leyenda_color(lf_analisis, COLOR_MUSGO, "Verde = persona con grado par")
        self._fila_leyenda_color(lf_analisis, COLOR_ORO, "Dorado = línea del camino Hamiltoniano")

        # Lista de personas con grado impar (se llena al calcular propiedades)
        self.lbl_titulo_impares = tk.Label(lf_analisis, text="", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                            font=(FUENTE_CUERPO, 8, "bold"))
        self.lbl_titulo_impares.pack(anchor="w", padx=10, pady=(6, 2))

        frame_lista_impares = tk.Frame(lf_analisis, bg=COLOR_FONDO)
        frame_lista_impares.pack(fill="x", padx=10, pady=(0, 4))

        scroll_impares = tk.Scrollbar(frame_lista_impares, orient="vertical")
        self.listbox_impares = tk.Listbox(frame_lista_impares, height=4, bg=COLOR_PAPEL, fg=COLOR_TINTA,
                                           font=(FUENTE_CUERPO, 8), selectbackground=COLOR_ORO,
                                           relief="flat", bd=0, highlightthickness=1,
                                           highlightbackground=COLOR_TINTA_SUAVE,
                                           yscrollcommand=scroll_impares.set)
        scroll_impares.config(command=self.listbox_impares.yview)
        self.listbox_impares.pack(side="left", fill="x", expand=True)
        scroll_impares.pack(side="right", fill="y")

        # SECCIÓN 2: Buscar Parentesco
        lf_camino = tk.LabelFrame(self.sidebar, text="  Buscar Parentesco  ", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                   font=(FUENTE_DISPLAY, 10, "bold"), bd=1, relief="solid")
        lf_camino.pack(fill="x", pady=6, ipady=4)

        f_selectores = tk.Frame(lf_camino, bg=COLOR_FONDO)
        f_selectores.pack(fill="x", padx=10, pady=2)
        
        tk.Label(f_selectores, text="De:", bg=COLOR_FONDO, fg=COLOR_PAPEL_OSCURO, font=(FUENTE_MONO, 8)).grid(row=0, column=0, sticky="w")
        self.om_persona_a = tk.OptionMenu(f_selectores, self.var_persona_a, "")
        self.om_persona_a.config(bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_ORO, relief="flat", font=(FUENTE_CUERPO, 8), width=24)
        self.om_persona_a.grid(row=0, column=1, padx=6, pady=2, sticky="we")

        tk.Label(f_selectores, text="A:", bg=COLOR_FONDO, fg=COLOR_PAPEL_OSCURO, font=(FUENTE_MONO, 8)).grid(row=1, column=0, sticky="w")
        self.om_persona_b = tk.OptionMenu(f_selectores, self.var_persona_b, "")
        self.om_persona_b.config(bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_ORO, relief="flat", font=(FUENTE_CUERPO, 8), width=24)
        self.om_persona_b.grid(row=1, column=1, padx=6, pady=2, sticky="we")

        f_botones_camino = tk.Frame(lf_camino, bg=COLOR_FONDO)
        f_botones_camino.pack(fill="x", padx=10, pady=4)
        self._boton_chico(f_botones_camino, "🔍  Ver Relación", self.ejecutar_busqueda_parentesco).pack(side="left")
        self._boton_chico(f_botones_camino, "🧹 Limpiar", self.limpiar_resaltados).pack(side="right")

        self.lbl_relacion_resultado = tk.Label(lf_camino, text="Selecciona personas y haz clic en buscar.", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                                font=(FUENTE_CUERPO, 8), wraplength=280, justify="left")
        self.lbl_relacion_resultado.pack(anchor="w", padx=10, pady=4)

        # SECCIÓN 3: Simulador de Propagación
        lf_sim = tk.LabelFrame(self.sidebar, text="  Simulación de Transmisión  ", bg=COLOR_FONDO, fg=COLOR_PAPEL,
                                font=(FUENTE_DISPLAY, 10, "bold"), bd=1, relief="solid")
        lf_sim.pack(fill="x", pady=6, ipady=4)

        f_sim_controles = tk.Frame(lf_sim, bg=COLOR_FONDO)
        f_sim_controles.pack(fill="x", padx=10, pady=2)

        tk.Label(f_sim_controles, text="Tipo:", bg=COLOR_FONDO, fg=COLOR_PAPEL_OSCURO, font=(FUENTE_MONO, 8)).grid(row=0, column=0, sticky="w")
        TIPOS_SIM = ["Apellido", "Contagio: Gripe", "Contagio: COVID-19",
                     "Contagio: Bacteria", "Genética Mendeliana", "Enfermedad Hereditaria"]
        self.om_sim_tipo = tk.OptionMenu(f_sim_controles, self.var_sim_tipo, *TIPOS_SIM, command=self._al_cambiar_tipo_sim)
        self.om_sim_tipo.config(bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_ORO, relief="flat", font=(FUENTE_CUERPO, 8), width=24)
        self.om_sim_tipo.grid(row=0, column=1, padx=6, pady=2, sticky="we")

        tk.Label(f_sim_controles, text="Origen:", bg=COLOR_FONDO, fg=COLOR_PAPEL_OSCURO, font=(FUENTE_MONO, 8)).grid(row=1, column=0, sticky="w")
        self.om_sim_origen = tk.OptionMenu(f_sim_controles, self.var_sim_origen, "")
        self.om_sim_origen.config(bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_ORO, relief="flat", font=(FUENTE_CUERPO, 8), width=24)
        self.om_sim_origen.grid(row=1, column=1, padx=6, pady=2, sticky="we")

        self.slider_prob = tk.Scale(lf_sim, from_=0.0, to=1.0, resolution=0.1, orient="horizontal",
                                     variable=self.var_sim_prob, label="Probabilidad de contagio",
                                     bg=COLOR_FONDO, fg=COLOR_PAPEL, highlightthickness=0,
                                     font=(FUENTE_MONO, 8), activebackground=COLOR_ORO)
        self.slider_prob.pack(fill="x", padx=10, pady=2)
        # Desactivado inicialmente porque "Apellido" no lo usa
        self.slider_prob.pack_forget()

        f_botones_sim = tk.Frame(lf_sim, bg=COLOR_FONDO)
        f_botones_sim.pack(fill="x", padx=10, pady=4)
        self._boton_chico(f_botones_sim, "🔥  Simular", self.ejecutar_simulacion).pack(side="left")
        self._boton_chico(f_botones_sim, "🧹 Reset", self.limpiar_simulacion).pack(side="right")

        # --- Panel de Estadísticas de Propagación ---
        lf_stats = tk.LabelFrame(lf_sim, text="  📊 Estadísticas en Tiempo Real  ",
                                  bg=COLOR_FONDO, fg=COLOR_ORO,
                                  font=(FUENTE_CUERPO, 8, "bold"), bd=1, relief="solid")
        lf_stats.pack(fill="x", padx=6, pady=(6, 4), ipady=4)

        self.txt_stats = tk.Text(lf_stats, height=6, wrap="word", state="disabled",
                                  bg="#FFFFFF", fg="#1A1A1A", bd=0,
                                  font=(FUENTE_MONO, 8), padx=8, pady=6,
                                  highlightthickness=0)
        self.txt_stats.pack(fill="x", padx=6, pady=4)
        self._stats_reset()

    def _boton(self, master, texto, comando):
        return tk.Button(master, text=texto, command=comando,
                          bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_ORO,
                          activeforeground=COLOR_TINTA, font=(FUENTE_MONO, 9), relief="flat",
                          padx=10, pady=6, cursor="hand2", bd=0)

    # -----------------------------------------------------------
    # Estadísticas de propagación
    # -----------------------------------------------------------
    def _stats_reset(self):
        """Limpia el panel de estadísticas y muestra el mensaje inicial."""
        self.txt_stats.config(state="normal")
        self.txt_stats.delete("1.0", "end")
        self.txt_stats.insert("end", "⏳ Esperando simulación...\nPresiona Simular para ver\nlas estadísticas en tiempo real.")
        self.txt_stats.config(state="disabled")

    def _stats_actualizar(self, pasos, idx_paso):
        """Actualiza el texto de estadísticas al finalizar la ronda idx_paso."""
        total_personas = len(self.arbol.nodos)
        if total_personas == 0:
            return

        # Acumular todos los nodos revelados hasta esta ronda
        infectados_acum = set()
        for i in range(idx_paso + 1):
            for nid in pasos[i]:
                infectados_acum.add(nid)

        total_infectados = len(infectados_acum)
        porcentaje = (total_infectados / total_personas) * 100

        self.txt_stats.config(state="normal")
        self.txt_stats.delete("1.0", "end")

        # Una línea por ronda ya transcurrida
        for i in range(idx_paso + 1):
            cant_ronda = len(pasos[i])
            self.txt_stats.insert("end", f"🔴 Ronda {i}: {cant_ronda} afectado{'s' if cant_ronda != 1 else ''}\n")

        self.txt_stats.insert("end", "-" * 28 + "\n")
        self.txt_stats.insert("end", f"🧬 Total: {total_infectados}/{total_personas} ({porcentaje:.1f}%)\n")

        if idx_paso + 1 >= len(pasos):
            sanos = total_personas - total_infectados
            self.txt_stats.insert("end", f"✅ Sanos: {sanos} | ✔ Simulación completa")

        self.txt_stats.config(state="disabled")
        # Desplazar al final
        self.txt_stats.see("end")

    # -----------------------------------------------------------
    # Layout
    # -----------------------------------------------------------
    def _recalcular_layout(self):
        filas = self.arbol.por_generacion()
        max_por_fila = max((len(v) for v in filas.values()), default=1)
        ancho = max(1000, max_por_fila * 190)
        alto = 160 + (self.arbol.generacion_maxima() + 1) * 170
        self.arbol.calcular_posiciones(ancho_lienzo=ancho, alto_fila=170)
        self.canvas.configure(scrollregion=(0, 0, ancho, alto))

    # -----------------------------------------------------------
    # Redibujo del grafo
    # -----------------------------------------------------------
    def _al_cambiar_pestaña(self, event):
        """Redibuja el grafo abstracto cada vez que el usuario entra a esa pestaña."""
        pestaña_actual = self.notebook.tab(self.notebook.select(), "text")
        if "Vista de Grafo" in pestaña_actual:
            self._dibujar_vista_grafo()
    # -----------------------------------------------------------
    # dibujo del grafo
    # -----------------------------------------------------------
    def _dibujar_vista_grafo(self):
        """Dibuja el grafo como circulos + lineas, resaltando grado impar y camino hamiltoniano."""
        self.canvas_grafo.delete("all")
        nodos = list(self.arbol.nodos.values())
        n = len(nodos)
        if n == 0:
            return

        import math
        radio = max(150, n * 20)
        cx, cy = radio + 60, radio + 60
        posiciones = {}
        for i, nodo in enumerate(nodos):
            ang = 2 * math.pi * i / n
            x = cx + radio * math.cos(ang)
            y = cy + radio * math.sin(ang)
            posiciones[nodo.id] = (x, y)

        self.canvas_grafo.configure(scrollregion=(0, 0, cx * 2 + 60, cy * 2 + 60))

        info = getattr(self, "info_grafo_actual", None) or self.arbol.analizar_propiedades_discretas()
        grados = self.arbol.obtener_grados()
        ruta_ham = info.get("ruta_hamiltoniana") or []
        aristas_ham = set(zip(ruta_ham, ruta_ham[1:]))

        dibujadas = set()
        for nodo in nodos:
            vecinos = list(nodo.hijos)
            if nodo.pareja:
                vecinos.append(nodo.pareja)
            for vecino in vecinos:
                clave = tuple(sorted([nodo.id, vecino.id]))
                if clave in dibujadas:
                    continue
                dibujadas.add(clave)
                x1, y1 = posiciones[nodo.id]
                x2, y2 = posiciones[vecino.id]
                en_camino = (nodo.id, vecino.id) in aristas_ham or (vecino.id, nodo.id) in aristas_ham
                color = COLOR_ORO if en_camino else COLOR_TINTA_SUAVE
                ancho = 3 if en_camino else 1
                self.canvas_grafo.create_line(x1, y1, x2, y2, fill=color, width=ancho)

        for nodo in nodos:
            x, y = posiciones[nodo.id]
            grado = grados[nodo.id]["total"]
            es_impar = grado % 2 != 0
            color_relleno = "#C0392B" if es_impar else COLOR_MUSGO
            self.canvas_grafo.create_oval(x - 22, y - 22, x + 22, y + 22,
                                           fill=color_relleno, outline=COLOR_PAPEL, width=2)
            self.canvas_grafo.create_text(x, y, text=nodo.nombre, fill=COLOR_PAPEL,
                                           font=(FUENTE_MONO, 8, "bold"))
            self.canvas_grafo.create_text(x, y + 32, text=f"grado {grado}", fill=COLOR_PAPEL_OSCURO,
                                           font=(FUENTE_MONO, 7))

    # -----------------------------------------------------------
    # Animación de construcción
    # -----------------------------------------------------------
    def _programar(self, ms, funcion):
        id_ = self.after(ms, funcion)
        self._despues_ids.append(id_)
        return id_

    def _cancelar_animaciones_pendientes(self):
        for id_ in self._despues_ids:
            try:
                self.after_cancel(id_)
            except Exception:
                pass
        self._despues_ids = []

    def reiniciar_animacion(self):
        self._cancelar_animaciones_pendientes()
        self._cache_puntos_rama = {}
        self.canvas.delete("all")
        self._recalcular_layout()
        generaciones = list(self.arbol.por_generacion().keys())
        self._animar_generacion(generaciones, 0)

    def _animar_generacion(self, generaciones, indice):
        if indice >= len(generaciones):
            return
        gen = generaciones[indice]
        personas = self.arbol.por_generacion()[gen]

        # 1) las tarjetas de esta generación aparecen escalonadas
        for i, persona in enumerate(personas):
            self._programar(i * 110, lambda p=persona: self._animar_aparicion_tarjeta(p))

        # 2) enlaces de pareja de personas de esta generación
        for a, b in self.arbol.parejas_unicas():
            if a.generacion == gen:
                self._programar(360, lambda a=a, b=b: self._dibujar_enlace_pareja(a, b))

        # 3) ramas que salen hacia la siguiente generación
        def iniciar_ramas():
            siguientes = [n for n in self.arbol.nodos.values()
                          if n.generacion == gen + 1 and n.padres]
            for hijo in siguientes:
                self._animar_rama_hacia(hijo)
        self._programar(480, iniciar_ramas)

        # 4) pasar a la siguiente generación
        self._programar(950, lambda: self._animar_generacion(generaciones, indice + 1))

    def _animar_aparicion_tarjeta(self, nodo, paso=0, pasos_totales=7):
        self.canvas.delete(f"tarjeta_{nodo.id}")
        escala = min((paso + 1) / pasos_totales, 1.0)
        self._dibujar_tarjeta(nodo, escala)
        if paso < pasos_totales - 1:
            self._programar(22, lambda: self._animar_aparicion_tarjeta(nodo, paso + 1, pasos_totales))

    def _animar_rama_hacia(self, nodo_hijo, paso=1, pasos_totales=16):
        punto_padres = self.arbol.punto_union_padres(nodo_hijo)
        if punto_padres is None:
            return

        if nodo_hijo.id not in self._cache_puntos_rama or paso == 1:
            x0, y0 = punto_padres
            y0 += 34
            x1, y1 = nodo_hijo.x, nodo_hijo.y - 6
            ctrl1 = (x0, (y0 + y1) / 2)
            ctrl2 = (x1, (y0 + y1) / 2)
            self._cache_puntos_rama[nodo_hijo.id] = curva_bezier((x0, y0), ctrl1, ctrl2, (x1, y1), pasos_totales)

        puntos = self._cache_puntos_rama[nodo_hijo.id]
        self.canvas.delete(f"rama_{nodo_hijo.id}")
        sub = puntos[:max(paso, 2)]
        plano = [coordenada for punto in sub for coordenada in punto]
        color_linea = COLOR_RAMA
        grosor_linea = 2.2
        if nodo_hijo.resaltado and any(p.resaltado for p in nodo_hijo.padres):
            color_linea = COLOR_ORO
            grosor_linea = 3.5

        self.canvas.create_line(*plano, fill=color_linea, width=grosor_linea, smooth=True,
                                 capstyle="round", tags=(f"rama_{nodo_hijo.id}", "rama"))

        if paso < len(puntos):
            self._programar(16, lambda: self._animar_rama_hacia(nodo_hijo, paso + 1, pasos_totales))
        else:
            self._cache_puntos_rama.pop(nodo_hijo.id, None)

    def _dibujar_enlace_pareja(self, a, b):
        color_linea = COLOR_ORO
        grosor_linea = 1.4
        es_guiones = (2, 4)
        if a.resaltado and b.resaltado:
            grosor_linea = 3.0
            es_guiones = None

        self.canvas.create_line(a.x, a.y, b.x, b.y, fill=color_linea, width=grosor_linea,
                                 dash=es_guiones, tags="pareja")
        mx, my = (a.x + b.x) / 2, (a.y + b.y) / 2
        self.canvas.create_oval(mx - 2.5, my - 2.5, mx + 2.5, my + 2.5,
                                 fill=COLOR_ORO, outline="", tags="pareja")

    # -----------------------------------------------------------
    # Dibujo de una tarjeta (persona)
    # -----------------------------------------------------------
    def _dibujar_tarjeta(self, nodo, escala=1.0):
        w, h = ANCHO_TARJETA * escala, ALTO_TARJETA * escala
        x0, y0 = nodo.x - w / 2, nodo.y - h / 2
        x1, y1 = nodo.x + w / 2, nodo.y + h / 2
        tag_nodo = f"tarjeta_{nodo.id}"

        # Decidir colores según el estado de simulación
        bg_color = COLOR_PAPEL
        border_color = COLOR_TINTA_SUAVE
        border_width = 1

        if nodo.resaltado:
            border_color = COLOR_ORO
            border_width = 3

        if nodo.estado_simulado:
            if nodo.estado_simulado == "infectado":
                bg_color = "#F2D7D5" # soft red
                if not nodo.resaltado:
                    border_color = "#A93226"
            elif nodo.estado_simulado == "sano":
                bg_color = "#D5F5E3" # soft green
                if not nodo.resaltado:
                    border_color = "#27AE60"
            elif nodo.estado_simulado.startswith("Ape:"):
                bg_color = "#D4E6F1" # soft blue
                if not nodo.resaltado:
                    border_color = "#2980B9"
            elif nodo.estado_simulado == "AA":
                bg_color = "#FADBD8" # afectado (rojo pálido)
                if not nodo.resaltado:
                    border_color = "#E74C3C"
            elif nodo.estado_simulado == "Aa":
                bg_color = "#FCF3CF" # portador (amarillo suave)
                if not nodo.resaltado:
                    border_color = "#F39C12"
            elif nodo.estado_simulado == "aa":
                bg_color = COLOR_PAPEL # normal

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color,
                                      outline=border_color, width=border_width,
                                      tags=(tag_nodo, nodo.id))
        self.canvas.create_oval(nodo.x - 3, y0 - 3, nodo.x + 3, y0 + 3, fill=COLOR_FONDO,
                                 outline=border_color, tags=(tag_nodo, nodo.id))

        if escala < 0.9:
            return  # el texto solo se dibuja cuando la tarjeta casi llegó a su tamaño final

        etiqueta = datos_prueba.ETIQUETAS_GENERACION.get(nodo.generacion, f"Generación {nodo.generacion}")
        self.canvas.create_text(nodo.x, y0 + 12, text=etiqueta.upper(),
                                 font=(FUENTE_MONO, 7), fill=COLOR_MUSGO, tags=(tag_nodo, nodo.id))

        # Género + año de nacimiento en esquina superior derecha
        icono_genero = "♂" if nodo.genero == "M" else "♀"
        color_genero = "#5B8FD6" if nodo.genero == "M" else "#D95FA0"
        fallecido = " †" if nodo.año_nacimiento < (2026 - 85) else ""
        self.canvas.create_text(x1 - 6, y0 + 9,
                                 text=f"{icono_genero} {nodo.año_nacimiento}{fallecido}",
                                 font=(FUENTE_MONO, 6), fill=color_genero,
                                 anchor="e", tags=(tag_nodo, nodo.id))

        self.canvas.create_text(nodo.x, y0 + 30, text=nodo.nombre,
                                 font=(FUENTE_DISPLAY, 12, "bold"), fill=COLOR_TINTA, tags=(tag_nodo, nodo.id))
        self.canvas.create_text(nodo.x, y0 + 46, text=nodo.apellido,
                                 font=(FUENTE_DISPLAY, 9, "italic"), fill=COLOR_TINTA_SUAVE,
                                 tags=(tag_nodo, nodo.id))

        # Si hay simulación activa, mostramos el estado de la simulación. Si no, mostramos el resumen.
        if nodo.estado_simulado:
            if nodo.estado_simulado == "infectado":
                texto_estado = "☣️ INFECTADO"
                color_estado = "#922B21"
            elif nodo.estado_simulado == "sano":
                texto_estado = "✅ SANO"
                color_estado = "#196F3D"
            elif nodo.estado_simulado.startswith("Ape:"):
                texto_estado = f"✍️ {nodo.estado_simulado}"
                color_estado = "#1A5276"
            elif nodo.estado_simulado in ("AA", "Aa", "aa"):
                gen_desc = {"AA": "Afectado (AA)", "Aa": "Portador (Aa)", "aa": "Sano (aa)"}[nodo.estado_simulado]
                texto_estado = f"🧬 {gen_desc}"
                color_estado = "#B9770E" if nodo.estado_simulado == "Aa" else ("#78281F" if nodo.estado_simulado == "AA" else "#1E8449")
            else:
                texto_estado = str(nodo.estado_simulado)
                color_estado = COLOR_TINTA_SUAVE

            self.canvas.create_text(nodo.x, y0 + 72, text=texto_estado.upper(),
                                     font=(FUENTE_MONO, 8, "bold"), fill=color_estado, tags=(tag_nodo, nodo.id))
        else:
            resumen = nodo.descripcion.split(". ")[0].strip()
            if len(resumen) > 42:
                resumen = resumen[:42].rstrip() + "…"
            elif not resumen.endswith("."):
                resumen += "."
            self.canvas.create_text(nodo.x, y0 + 72, text=resumen, width=w - 12,
                                     font=(FUENTE_CUERPO, 8), fill=COLOR_TINTA_SUAVE, tags=(tag_nodo, nodo.id))

    # -----------------------------------------------------------
    # Interacción: clic para ver ficha completa
    # -----------------------------------------------------------
    def _al_hacer_clic(self, evento):
        x = self.canvas.canvasx(evento.x)
        y = self.canvas.canvasy(evento.y)
        for item in self.canvas.find_overlapping(x, y, x, y):
            id_nodo = next((t for t in self.canvas.gettags(item) if t in self.arbol.nodos), None)
            if id_nodo:
                self._mostrar_ficha(self.arbol.nodos[id_nodo])
                return

    def _mostrar_ficha(self, nodo):
        ventana = tk.Toplevel(self)
        ventana.title(nodo.nombre_completo())
        ventana.configure(bg=COLOR_PAPEL)
        ventana.resizable(True, True)
        ventana.minsize(380, 420)
        ventana.geometry(f"430x520+{self.winfo_rootx() + 90}+{self.winfo_rooty() + 80}")

        # Configurar expansión al redimensionar
        ventana.rowconfigure(0, weight=0)   # encabezado fijo
        ventana.rowconfigure(1, weight=0)   # datos salud fijo
        ventana.rowconfigure(2, weight=1)   # descripción expande
        ventana.rowconfigure(3, weight=0)   # botón fijo
        ventana.columnconfigure(0, weight=1)

        # --- ENCABEZADO ---
        frm_header = tk.Frame(ventana, bg=COLOR_PAPEL)
        frm_header.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 4))

        etiqueta = datos_prueba.ETIQUETAS_GENERACION.get(nodo.generacion, f"Generación {nodo.generacion}")
        tk.Label(frm_header, text=etiqueta.upper(), bg=COLOR_PAPEL, fg=COLOR_MUSGO,
                 font=(FUENTE_MONO, 9)).pack(anchor="w")
        tk.Label(frm_header, text=nodo.nombre, bg=COLOR_PAPEL, fg=COLOR_TINTA,
                 font=(FUENTE_DISPLAY, 20, "bold")).pack(anchor="w")
        tk.Label(frm_header, text=nodo.apellido, bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_DISPLAY, 13, "italic")).pack(anchor="w")

        # --- SEPARADOR ---
        tk.Frame(ventana, bg=COLOR_RAMA, height=1).grid(row=0, column=0, sticky="sew",
                                                         padx=22, pady=(0, 0))

        # --- DATOS DE SALUD ---
        AÑO_ACTUAL = 2026
        es_fallecido = nodo.año_nacimiento < (AÑO_ACTUAL - 85)
        icono_genero = "♂ Hombre" if nodo.genero == "M" else "♀ Mujer"
        estado_vital = f"✝ Fallecido" if es_fallecido else "Vivo/a"
        color_vital = "#888" if es_fallecido else "#27AE60"

        frm_salud = tk.LabelFrame(ventana, text="  Datos de Salud e Inmunidad  ", bg=COLOR_PAPEL,
                                   fg=COLOR_TINTA_SUAVE, font=(FUENTE_MONO, 8),
                                   bd=1, relief="solid")
        frm_salud.grid(row=1, column=0, sticky="ew", padx=22, pady=10)
        frm_salud.columnconfigure(1, weight=1)

        # Género
        tk.Label(frm_salud, text="⚧  Género:", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 9, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=2)
        tk.Label(frm_salud, text=icono_genero, bg=COLOR_PAPEL, fg=COLOR_TINTA,
                 font=(FUENTE_CUERPO, 10)).grid(row=0, column=1, sticky="w", padx=6, pady=2)

        # Año de nacimiento + estado vital
        tk.Label(frm_salud, text="📅  Nacimiento:", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 9, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=2)
        tk.Label(frm_salud, text=f"{nodo.año_nacimiento}  —  {estado_vital}",
                 bg=COLOR_PAPEL, fg=color_vital,
                 font=(FUENTE_CUERPO, 10)).grid(row=1, column=1, sticky="w", padx=6, pady=2)

        # Función auxiliar para barra de inmunidad
        def barra_inmunidad(frame, fila, etiqueta, valor, emoji):
            pct = int(valor * 100)
            barra = "█" * (pct // 10) + "░" * (10 - pct // 10)
            color = "#27AE60" if pct >= 65 else ("#E67E22" if pct >= 35 else "#E74C3C")
            tk.Label(frame, text=f"{emoji}  {etiqueta}:", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                     font=(FUENTE_MONO, 9, "bold")).grid(row=fila, column=0, sticky="w", padx=10, pady=2)
            tk.Label(frame, text=f"{barra}  {pct}%", bg=COLOR_PAPEL, fg=color,
                     font=(FUENTE_MONO, 9)).grid(row=fila, column=1, sticky="w", padx=6, pady=2)

        barra_inmunidad(frm_salud, 2, "Inmunidad Gripe",    nodo.inmune_gripe,    "🤧")
        barra_inmunidad(frm_salud, 3, "Inmunidad COVID-19", nodo.inmune_covid,    "🦠")
        barra_inmunidad(frm_salud, 4, "Inmunidad Bacteria", nodo.inmune_bacteria, "🧫")

        # --- DESCRIPCIÓN con scroll (expande al agrandar la ventana) ---
        frm_desc = tk.Frame(ventana, bg=COLOR_PAPEL)
        frm_desc.grid(row=2, column=0, sticky="nsew", padx=22, pady=(4, 4))
        frm_desc.rowconfigure(0, weight=1)
        frm_desc.columnconfigure(0, weight=1)

        txt_desc = tk.Text(frm_desc, wrap="word", font=(FUENTE_CUERPO, 11),
                            bg=COLOR_PAPEL_OSCURO, fg=COLOR_TINTA, relief="flat",
                            padx=10, pady=8, cursor="arrow",
                            state="normal", highlightthickness=1,
                            highlightbackground=COLOR_TINTA_SUAVE)
        scroll_desc = tk.Scrollbar(frm_desc, orient="vertical", command=txt_desc.yview)
        txt_desc.configure(yscrollcommand=scroll_desc.set)

        txt_desc.insert("1.0", nodo.descripcion)
        txt_desc.config(state="disabled")  # solo lectura

        txt_desc.grid(row=0, column=0, sticky="nsew")
        scroll_desc.grid(row=0, column=1, sticky="ns")

        # --- BOTÓN CERRAR (anclado abajo) ---
        self._boton(ventana, "Cerrar", ventana.destroy).grid(
            row=3, column=0, sticky="e", padx=22, pady=(4, 14)
        )

    # -----------------------------------------------------------
    # Agregar / quitar personas
    def al_confirmar_agregar(self):
        self.reiniciar_animacion()
        self._actualizar_opciones_sidebar()

    def abrir_dialogo_agregar(self):
        DialogoAgregarPersona(self, self.arbol, al_confirmar=self.al_confirmar_agregar)

    def abrir_dialogo_generar_aleatorio(self):
        DialogoGenerarAleatorio(self, self.arbol, al_confirmar=self.al_confirmar_agregar)

    def quitar_ultima(self):
        if not self.arbol.nodos:
            return
        if self.arbol.quitar_ultima_persona():
            self.reiniciar_animacion()
            self._actualizar_opciones_sidebar()

    # -----------------------------------------------------------
    # Métodos y Acciones del Panel Lateral
    # -----------------------------------------------------------
    def _boton_chico(self, master, texto, comando):
        return tk.Button(master, text=texto, command=comando,
                          bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_ORO,
                          activeforeground=COLOR_TINTA, font=(FUENTE_MONO, 8), relief="flat",
                          padx=6, pady=4, cursor="hand2", bd=0)
    
    def _fila_leyenda_color(self, master, color_hex, texto):
        """Crea una fila con un círculo de color real (no emoji) + texto explicativo."""
        fila = tk.Frame(master, bg=COLOR_FONDO)
        fila.pack(anchor="w", padx=10, pady=1, fill="x")

        mini_canvas = tk.Canvas(fila, width=14, height=14, bg=COLOR_FONDO, highlightthickness=0)
        mini_canvas.create_oval(1, 1, 13, 13, fill=color_hex, outline="")
        mini_canvas.pack(side="left", padx=(0, 6))

        tk.Label(fila, text=texto, bg=COLOR_FONDO, fg=COLOR_PAPEL_OSCURO,
                 font=(FUENTE_CUERPO, 8), justify="left", wraplength=250, anchor="w"
                 ).pack(side="left", fill="x", expand=True)

    def _al_cambiar_tipo_sim(self, valor):
        if valor.startswith("Contagio:"):
            self.slider_prob.pack(fill="x", padx=10, pady=2)
        else:
            self.slider_prob.pack_forget()

    def _actualizar_opciones_sidebar(self):
        opciones = [f"{n.nombre_completo()} ({n.id})" for n in self.arbol.nodos.values()]
        
        menu_a = self.om_persona_a["menu"]
        menu_b = self.om_persona_b["menu"]
        menu_ori = self.om_sim_origen["menu"]
        
        menu_a.delete(0, "end")
        menu_b.delete(0, "end")
        menu_ori.delete(0, "end")
        
        for opcion in opciones:
            menu_a.add_command(label=opcion, command=lambda val=opcion: self.var_persona_a.set(val))
            menu_b.add_command(label=opcion, command=lambda val=opcion: self.var_persona_b.set(val))
            menu_ori.add_command(label=opcion, command=lambda val=opcion: self.var_sim_origen.set(val))
            
        if opciones:
            self.var_persona_a.set(opciones[0])
            self.var_persona_b.set(opciones[1] if len(opciones) > 1 else opciones[0])
            self.var_sim_origen.set(opciones[0])
        else:
            self.var_persona_a.set("")
            self.var_persona_b.set("")
            self.var_sim_origen.set("")

    def redibujar_arbol_completo(self):
        self._cancelar_animaciones_pendientes()
        self._cache_puntos_rama = {}
        self.canvas.delete("all")
        self._recalcular_layout()
        
        # 1. Dibujar todas las ramas parent-child
        for nodo in self.arbol.nodos.values():
            if nodo.padres:
                punto_padres = self.arbol.punto_union_padres(nodo)
                if punto_padres:
                    x0, y0 = punto_padres
                    y0 += 34
                    x1, y1 = nodo.x, nodo.y - 6
                    ctrl1 = (x0, (y0 + y1) / 2)
                    ctrl2 = (x1, (y0 + y1) / 2)
                    puntos = curva_bezier((x0, y0), ctrl1, ctrl2, (x1, y1), 16)
                    plano = [coordenada for punto in puntos for coordenada in punto]
                    
                    color_linea = COLOR_RAMA
                    grosor_linea = 2.2
                    if nodo.resaltado and any(p.resaltado for p in nodo.padres):
                        color_linea = COLOR_ORO
                        grosor_linea = 3.5
                        
                    self.canvas.create_line(*plano, fill=color_linea, width=grosor_linea, smooth=True,
                                             capstyle="round", tags=(f"rama_{nodo.id}", "rama"))

        # 2. Dibujar enlaces de parejas
        for a, b in self.arbol.parejas_unicas():
            color_linea = COLOR_ORO
            grosor_linea = 1.4
            es_guiones = (2, 4)
            if a.resaltado and b.resaltado:
                grosor_linea = 3.0
                es_guiones = None
                
            self.canvas.create_line(a.x, a.y, b.x, b.y, fill=color_linea, width=grosor_linea,
                                     dash=es_guiones, tags="pareja")
            mx, my = (a.x + b.x) / 2, (a.y + b.y) / 2
            self.canvas.create_oval(mx - 2.5, my - 2.5, mx + 2.5, my + 2.5,
                                     fill=COLOR_ORO, outline="", tags="pareja")

        # 3. Dibujar tarjetas
        for nodo in self.arbol.nodos.values():
            self._dibujar_tarjeta(nodo, escala=1.0)

    def abrir_dialogo_matriz(self):
        try:
            nodos_ids, matriz = self.arbol.generar_matriz_adyacencia()
        except AttributeError:
            messagebox.showinfo("No implementado", "El método de matriz de adyacencia aún no está disponible.")
            return

        if not nodos_ids:
            messagebox.showinfo("Árbol vacío", "No hay personas en el árbol para mostrar la matriz.")
            return

        dialogo = tk.Toplevel(self)
        dialogo.title("Matriz de Adyacencia Dirigida")
        dialogo.configure(bg=COLOR_PAPEL)
        dialogo.geometry("600x500")
        # Centrar sobre la ventana principal
        dialogo.geometry(f"+{self.winfo_rootx() + 50}+{self.winfo_rooty() + 50}")

        lbl_titulo = tk.Label(dialogo, text="MATRIZ DE ADYACENCIA", bg=COLOR_PAPEL, fg=COLOR_TINTA, font=(FUENTE_DISPLAY, 14, "bold"))
        lbl_titulo.pack(pady=10)

        lbl_desc = tk.Label(dialogo, text="Un '1' indica que la persona en la fila es progenitor/a de la persona en la columna.\nMostrando los IDs truncados.",
                            bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE, font=(FUENTE_CUERPO, 9))
        lbl_desc.pack(pady=(0, 10))

        frame_txt = tk.Frame(dialogo, bg=COLOR_PAPEL)
        frame_txt.pack(fill="both", expand=True, padx=15, pady=10)

        txt = tk.Text(frame_txt, wrap="none", font=(FUENTE_MONO, 10), bg=COLOR_PAPEL_OSCURO, fg=COLOR_TINTA, bd=0, padx=10, pady=10)
        h_scroll = tk.Scrollbar(frame_txt, orient="horizontal", command=txt.xview)
        v_scroll = tk.Scrollbar(frame_txt, orient="vertical", command=txt.yview)
        txt.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        txt.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        frame_txt.rowconfigure(0, weight=1)
        frame_txt.columnconfigure(0, weight=1)

        # Construir texto de la matriz
        # Encabezados
        header = f"{'Nombre':<12}"
        nombres_cortos = [self.arbol.nodos[nid].nombre[:8] for nid in nodos_ids]
        
        for nom in nombres_cortos:
            header += f"{nom:^9}"
        header += "\n" + "-" * len(header) + "\n"
        
        txt.insert("end", header)

        for i, row in enumerate(matriz):
            fila_txt = f"{nombres_cortos[i]:<12}"
            for val in row:
                fila_txt += f"{val:^9}"
            txt.insert("end", fila_txt + "\n")

        txt.config(state="disabled")

        btn_cerrar = tk.Button(dialogo, text="Cerrar", command=dialogo.destroy, bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO,
                               font=(FUENTE_MONO, 9), cursor="hand2", relief="flat", padx=15, pady=6)
        btn_cerrar.pack(pady=15)

    def ejecutar_analisis(self):
        propiedades = self.arbol.analizar_propiedades_discretas()
        
        texto_nodos_edges = f"Nodos (Personas): {propiedades['nodos']}  |  Aristas (Relaciones): {propiedades['aristas']}"
        texto_dag_conexo = f"¿Es DAG (relación biológica sin ciclos)? {'Sí (Válido)' if propiedades['dag'] else 'No (Incorrecto)'}\n¿Toda la familia está conectada? {'Sí (Conexo)' if propiedades['conexo'] else 'No (Bosque)'}"
        
        explicacion_euler_hamilton = ""
        cant_impares = propiedades['cantidad_nodos_impares']
        nombres_impares = propiedades['nombres_nodos_impares']

        if propiedades['euleriano']:
            explicacion_euler_hamilton += (
                f"• Camino Euleriano: Existe (todas las personas tienen grado par, "
                f"o hay exactamente 2 con grado impar).\n"
            )
        else:
            if cant_impares > 2:
                explicacion_euler_hamilton += (
                    f"• Camino Euleriano: No existe. Hay {cant_impares} personas con grado "
                    f"impar (deberían ser 0 o 2, ver lista abajo).\n"
                )
            else:
                explicacion_euler_hamilton += (
                    f"• Camino Euleriano: No existe (el árbol no está totalmente conectado).\n"
                )

        if propiedades['hamiltoniano']:
            explicacion_euler_hamilton += "• Camino Hamiltoniano: Existe — resaltado en dorado en la pestaña 'Vista de Grafo'.\n"
        else:
            explicacion_euler_hamilton += "• Camino Hamiltoniano: No existe (las ramificaciones lo impiden; no hay forma de visitar a todos sin repetir).\n"

        # Llenar la lista de personas con grado impar
        self.listbox_impares.delete(0, tk.END)
        if cant_impares > 0:
            self.lbl_titulo_impares.config(text=f"Personas con grado impar ({cant_impares}):")
            for nombre in nombres_impares:
                self.listbox_impares.insert(tk.END, f"• {nombre}")
        else:
            self.lbl_titulo_impares.config(text="Personas con grado impar: ninguna ✔")
            
        texto_grados = f"Persona con más relaciones: {propiedades['max_grado_nombre']} (Grado: {propiedades['max_grado']})"
        
        self.lbl_nodos_edges.config(text=texto_nodos_edges, fg=COLOR_PAPEL)
        self.lbl_dag_conexo.config(text=texto_dag_conexo, fg=COLOR_PAPEL)
        self.lbl_euler_hamilton.config(text=explicacion_euler_hamilton + texto_grados, fg=COLOR_PAPEL_OSCURO)

        # Guardar el resultado y saltar a la pestaña "Vista de Grafo"
        self.info_grafo_actual = propiedades
        self.notebook.select(1)   # dispara _al_cambiar_pestaña, que llama a _dibujar_vista_grafo

    def ejecutar_busqueda_parentesco(self):
        # Limpiar cualquier resaltado anterior
        for n in self.arbol.nodos.values():
            n.resaltado = False
            
        id_a_texto = self.var_persona_a.get()
        id_b_texto = self.var_persona_b.get()
        
        if not id_a_texto or not id_b_texto:
            messagebox.showwarning("Selección incompleta", "Por favor selecciona dos personas.")
            return
            
        id_a = id_a_texto.split("(")[-1].rstrip(")")
        id_b = id_b_texto.split("(")[-1].rstrip(")")
        
        camino, descripcion = self.arbol.buscar_camino_parentesco(id_a, id_b)
        
        if camino:
            for nid in camino:
                self.arbol.nodos[nid].resaltado = True
            # Mostrar la relación de parentesco traducida
            self.lbl_relacion_resultado.config(text=descripcion, fg=COLOR_BOTON_TEXTO)
            self.redibujar_arbol_completo()
        else:
            self.lbl_relacion_resultado.config(text=descripcion, fg="#EC7063")

    def limpiar_resaltados(self):
        for n in self.arbol.nodos.values():
            n.resaltado = False
        self.lbl_relacion_resultado.config(text="Selecciona personas y haz clic en buscar.", fg=COLOR_PAPEL)
        self.redibujar_arbol_completo()

    def ejecutar_simulacion(self):
        self.limpiar_simulacion()
        
        tipo = self.var_sim_tipo.get()
        id_origen_texto = self.var_sim_origen.get()
        
        if not id_origen_texto:
            messagebox.showwarning("Selección incompleta", "Por favor selecciona una persona de origen.")
            return
            
        id_origen = id_origen_texto.split("(")[-1].rstrip(")")

        # Mapeo tipo -> clave de enfermedad
        MAPA_ENFERMEDAD = {
            "Contagio: Gripe":    "gripe",
            "Contagio: COVID-19": "covid",
            "Contagio: Bacteria": "bacteria",
        }
        
        if tipo == "Apellido":
            pasos = self.arbol.simular_propagacion_apellido(id_origen)
        elif tipo in MAPA_ENFERMEDAD:
            prob = self.var_sim_prob.get()
            pasos = self.arbol.simular_propagacion_contagio(id_origen, prob, MAPA_ENFERMEDAD[tipo])
        elif tipo == "Genética Mendeliana":
            pasos = self.arbol.simular_propagacion_genetica(id_origen)
        elif tipo == "Enfermedad Hereditaria":
            pasos = self.arbol.simular_propagacion_multifactorial(id_origen)
        else:
            return
            
        if not pasos:
            messagebox.showinfo("Simulación terminada", "No se propagó a ninguna persona.")
            return
            
        self._animar_pasos_simulacion(pasos, 0)

    def _animar_pasos_simulacion(self, pasos, idx_paso):
        if idx_paso >= len(pasos):
            return
            
        # Revelar nodos hasta el paso actual
        nodos_revelados = set()
        for i in range(idx_paso + 1):
            for nid in pasos[i]:
                nodos_revelados.add(nid)
                
        tipo = self.var_sim_tipo.get()
        es_contagio = tipo.startswith("Contagio:")
        es_genetica = tipo == "Genética Mendeliana"
        es_hereditaria = tipo == "Enfermedad Hereditaria"

        # Guardar estados originales para aplicar selectivamente
        estados_temporales = {}
        for nid, nodo in self.arbol.nodos.items():
            estados_temporales[nid] = nodo.estado_simulado
            if nid not in nodos_revelados:
                if es_contagio or es_hereditaria:
                    nodo.estado_simulado = "sano"
                elif es_genetica:
                    nodo.estado_simulado = "aa"
                else:
                    nodo.estado_simulado = None
                    
        self.redibujar_arbol_completo()
        
        # Restaurar estados reales
        for nid, nodo in self.arbol.nodos.items():
            nodo.estado_simulado = estados_temporales[nid]

        # Actualizar estadísticas de esta ronda
        self._stats_actualizar(pasos, idx_paso)
            
        # Siguiente ronda
        self._programar(800, lambda: self._animar_pasos_simulacion(pasos, idx_paso + 1))

    def limpiar_simulacion(self):
        for n in self.arbol.nodos.values():
            n.estado_simulado = None
        self.redibujar_arbol_completo()
        self._stats_reset()


class DialogoAgregarPersona(tk.Toplevel):
    """Formulario para crear un Nodo nuevo y conectarlo con padres / pareja existentes."""

    def __init__(self, master, arbol, al_confirmar):
        super().__init__(master)
        self.arbol = arbol
        self.al_confirmar = al_confirmar
        self._ids_en_orden = list(arbol.nodos.keys())

        self.title("Agregar persona")
        self.configure(bg=COLOR_PAPEL)
        self.resizable(False, False)
        self.geometry(f"+{master.winfo_rootx() + 100}+{master.winfo_rooty() + 80}")
        self.grab_set()  # ventana modal

        campos = tk.Frame(self, bg=COLOR_PAPEL, padx=22, pady=20)
        campos.pack(fill="both", expand=True)

        self.var_nombre        = tk.StringVar()
        self.var_apellido      = tk.StringVar()
        self.var_generacion    = tk.IntVar(value=arbol.generacion_maxima() + 1)
        self.var_año_nac       = tk.IntVar(value=2000)
        self.var_genero        = tk.StringVar(value="M")
        self.var_inmune_gripe  = tk.DoubleVar(value=0.5)
        self.var_inmune_covid  = tk.DoubleVar(value=0.5)
        self.var_inmune_bact   = tk.DoubleVar(value=0.5)

        self._campo_texto(campos, "Nombre", self.var_nombre, 0)
        self._campo_texto(campos, "Apellido(s)", self.var_apellido, 1)

        # Generación
        tk.Label(campos, text="Generación (0 = más antigua)", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 8)).grid(row=2, column=0, sticky="w", pady=(8, 2))
        tk.Spinbox(campos, from_=0, to=20, textvariable=self.var_generacion, width=6,
                   font=(FUENTE_CUERPO, 10)).grid(row=2, column=1, sticky="w", pady=(8, 2))

        # Género
        tk.Label(campos, text="Género", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 8)).grid(row=3, column=0, sticky="w", pady=(8, 2))
        frm_gen = tk.Frame(campos, bg=COLOR_PAPEL)
        frm_gen.grid(row=3, column=1, sticky="w", pady=(8, 2))
        tk.Radiobutton(frm_gen, text="♂ Hombre", variable=self.var_genero, value="M",
                       bg=COLOR_PAPEL, fg=COLOR_TINTA, font=(FUENTE_CUERPO, 9),
                       selectcolor=COLOR_PAPEL_OSCURO).pack(side="left")
        tk.Radiobutton(frm_gen, text="♀ Mujer", variable=self.var_genero, value="F",
                       bg=COLOR_PAPEL, fg=COLOR_TINTA, font=(FUENTE_CUERPO, 9),
                       selectcolor=COLOR_PAPEL_OSCURO).pack(side="left", padx=8)

        # Año de nacimiento
        tk.Label(campos, text="Año de nacimiento", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 8)).grid(row=4, column=0, sticky="w", pady=(8, 2))
        tk.Spinbox(campos, from_=1840, to=2026, textvariable=self.var_año_nac, width=8,
                   font=(FUENTE_CUERPO, 10)).grid(row=4, column=1, sticky="w", pady=(8, 2))

        # Inmunidades específicas
        def _slider_inmune(fila, label, var):
            tk.Label(campos, text=label, bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                     font=(FUENTE_MONO, 8)).grid(row=fila, column=0, columnspan=2, sticky="w", pady=(6, 0))
            frm = tk.Frame(campos, bg=COLOR_PAPEL)
            frm.grid(row=fila + 1, column=0, columnspan=2, sticky="we", pady=(0, 2))
            tk.Scale(frm, from_=0.0, to=1.0, resolution=0.05, orient="horizontal",
                     variable=var, bg=COLOR_PAPEL, fg=COLOR_TINTA, highlightthickness=0,
                     font=(FUENTE_MONO, 7), activebackground=COLOR_ORO, length=220).pack(side="left")
            tk.Label(frm, textvariable=var, bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                     font=(FUENTE_MONO, 8, "bold")).pack(side="left", padx=4)

        _slider_inmune(5,  "🤧  Inmunidad Gripe (0=ninguna · 1=total)",    self.var_inmune_gripe)
        _slider_inmune(7,  "🦠  Inmunidad COVID-19",                        self.var_inmune_covid)
        _slider_inmune(9,  "🧫  Inmunidad Bacteria",                        self.var_inmune_bact)

        # Descripción
        tk.Label(campos, text="Descripción", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 8)).grid(row=11, column=0, columnspan=2, sticky="w", pady=(10, 2))
        self.texto_descripcion = tk.Text(campos, width=42, height=3, font=(FUENTE_CUERPO, 10), wrap="word")
        self.texto_descripcion.grid(row=12, column=0, columnspan=2, sticky="w")

        # Padres (exactamente 2, que sean pareja entre sí)
        tk.Label(campos, text="Padres — selecciona exactamente 2 que sean pareja",
                 bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE, font=(FUENTE_MONO, 8)
                 ).grid(row=13, column=0, columnspan=2, sticky="w", pady=(12, 2))
        self.lista_padres = tk.Listbox(campos, selectmode="multiple", exportselection=False,
                                        height=4, font=(FUENTE_CUERPO, 10))
        for id_persona in self._ids_en_orden:
            nodo = arbol.nodos[id_persona]
            icono = "♂" if nodo.genero == "M" else "♀"
            self.lista_padres.insert("end", f"{icono} {nodo.nombre_completo()}  ({id_persona}) — {nodo.año_nacimiento}")
        self.lista_padres.grid(row=14, column=0, columnspan=2, sticky="we")

        # Pareja (opcional, para este nodo)
        tk.Label(campos, text="Pareja (opcional)", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 8)).grid(row=15, column=0, columnspan=2, sticky="w", pady=(12, 2))
        opciones_pareja = ["(ninguna)"] + [
            f"{arbol.nodos[i].nombre_completo()}  ({i})"
            for i in self._ids_en_orden
        ]
        self.var_pareja = tk.StringVar(value="(ninguna)")
        tk.OptionMenu(campos, self.var_pareja, *opciones_pareja).grid(row=16, column=0, columnspan=2, sticky="w")

        botones = tk.Frame(campos, bg=COLOR_PAPEL)
        botones.grid(row=17, column=0, columnspan=2, sticky="e", pady=(18, 0))
        tk.Button(botones, text="Cancelar", command=self.destroy, bg=COLOR_PAPEL_OSCURO,
                  fg=COLOR_TINTA, relief="flat", padx=10, pady=5).pack(side="right", padx=(6, 0))
        tk.Button(botones, text="Agregar", command=self._confirmar, bg=COLOR_ORO,
                  fg=COLOR_TINTA, relief="flat", padx=10, pady=5).pack(side="right")

    def _campo_texto(self, master, etiqueta, variable, fila):
        tk.Label(master, text=etiqueta, bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 8)).grid(row=fila, column=0, sticky="w", pady=(0, 2))
        tk.Entry(master, textvariable=variable, width=30, font=(FUENTE_CUERPO, 10)
                  ).grid(row=fila, column=1, sticky="w", pady=(0, 2))

    def _confirmar(self):
        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        descripcion = self.texto_descripcion.get("1.0", "end").strip() or "Sin descripción registrada."

        if not nombre or not apellido:
            messagebox.showwarning("Faltan datos", "Nombre y apellido son obligatorios.", parent=self)
            return

        seleccion = self.lista_padres.curselection()
        padres_ids = [self._ids_en_orden[i] for i in seleccion]

        # Validar: si se seleccionaron padres, deben ser exactamente 2
        if len(padres_ids) not in (0, 2):
            messagebox.showwarning("Selección de padres",
                                   "Debes seleccionar exactamente 2 padres (o ninguno si no tiene padres en el árbol).",
                                   parent=self)
            return

        # Validar: los 2 padres deben ser pareja entre sí y de diferente género
        if len(padres_ids) == 2:
            p1 = self.arbol.nodos[padres_ids[0]]
            p2 = self.arbol.nodos[padres_ids[1]]
            if p1.pareja != p2:
                messagebox.showwarning("Padres inválidos",
                                       f"{p1.nombre} y {p2.nombre} no son pareja entre sí.\nSolo parejas registradas pueden tener hijos en el árbol.",
                                       parent=self)
                return
            if p1.genero == p2.genero:
                messagebox.showwarning("Padres inválidos",
                                       "Los dos padres deben ser de diferente género (uno ♂ y una ♀).",
                                       parent=self)
                return
            # Validar diferencia de año de nacimiento >= 17
            año_hijo = self.var_año_nac.get()
            año_padre_mayor = max(p1.año_nacimiento, p2.año_nacimiento)
            if año_hijo - año_padre_mayor < 17:
                messagebox.showwarning("Año de nacimiento inválido",
                                       f"El hijo debe nacer al menos 17 años después del padre/madre más joven.\nAño mínimo permitido: {año_padre_mayor + 17}.",
                                       parent=self)
                return

        pareja_texto = self.var_pareja.get()
        pareja_id = None
        if pareja_texto != "(ninguna)":
            pareja_id = pareja_texto.split("(")[-1].rstrip(")")

        nuevo_id = self.arbol.siguiente_id_disponible()
        self.arbol.agregar_persona(
            id_persona=nuevo_id, nombre=nombre, apellido=apellido,
            descripcion=descripcion, generacion=self.var_generacion.get(),
            padres_ids=padres_ids, pareja_id=pareja_id,
            genero=self.var_genero.get(),
            año_nacimiento=self.var_año_nac.get(),
            inmune_gripe=round(self.var_inmune_gripe.get(), 2),
            inmune_covid=round(self.var_inmune_covid.get(), 2),
            inmune_bacteria=round(self.var_inmune_bact.get(), 2),
        )
        self.destroy()
        self.al_confirmar()


class DialogoGenerarAleatorio(tk.Toplevel):
    """Formulario para ingresar X (personas) y H (pisos/generaciones) y generar un árbol aleatorio."""

    def __init__(self, master, arbol, al_confirmar):
        super().__init__(master)
        self.arbol = arbol
        self.al_confirmar = al_confirmar

        self.title("Generar árbol aleatorio")
        self.configure(bg=COLOR_PAPEL)
        self.resizable(False, False)
        self.geometry(f"+{master.winfo_rootx() + 100}+{master.winfo_rooty() + 80}")
        self.grab_set()  # ventana modal

        campos = tk.Frame(self, bg=COLOR_PAPEL, padx=22, pady=20)
        campos.pack(fill="both", expand=True)

        self.var_personas = tk.IntVar(value=15)
        self.var_pisos = tk.IntVar(value=5)

        tk.Label(campos, text="Número de personas (X)", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 9, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 2))
        tk.Entry(campos, textvariable=self.var_personas, width=15, font=(FUENTE_CUERPO, 10)
                 ).grid(row=0, column=1, sticky="w", pady=(0, 2), padx=(10, 0))

        tk.Label(campos, text="Número de pisos / gen (H)", bg=COLOR_PAPEL, fg=COLOR_TINTA_SUAVE,
                 font=(FUENTE_MONO, 9, "bold")).grid(row=1, column=0, sticky="w", pady=(8, 2))
        tk.Entry(campos, textvariable=self.var_pisos, width=15, font=(FUENTE_CUERPO, 10)
                 ).grid(row=1, column=1, sticky="w", pady=(8, 2), padx=(10, 0))

        # Nota aclaratoria sobre la validación X >= 2H-1
        tk.Label(campos,
                 text="Restricciones:\n• Parejas heterosexuales obligatorias\n• Mínimo 17 años entre padres e hijos\n• Se requiere X ≥ 2H−1 (ej: 5 pisos → mínimo 9 personas)",
                 bg=COLOR_PAPEL, fg=COLOR_MUSGO, font=(FUENTE_CUERPO, 8, "italic"), justify="left"
                 ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))

        botones = tk.Frame(campos, bg=COLOR_PAPEL)
        botones.grid(row=3, column=0, columnspan=2, sticky="e", pady=(18, 0))
        
        tk.Button(botones, text="Cancelar", command=self.destroy, bg=COLOR_PAPEL_OSCURO,
                  fg=COLOR_TINTA, relief="flat", padx=10, pady=5).pack(side="right", padx=(6, 0))
        tk.Button(botones, text="Generar", command=self._confirmar, bg=COLOR_ORO,
                  fg=COLOR_TINTA, relief="flat", padx=10, pady=5).pack(side="right")

    def _confirmar(self):
        try:
            x = self.var_personas.get()
            h = self.var_pisos.get()
        except tk.TclError:
            messagebox.showwarning("Datos inválidos", "Por favor ingresa números enteros válidos.", parent=self)
            return

        if x <= 0 or h <= 0:
            messagebox.showwarning("Datos inválidos", "Los números de personas y pisos deben ser mayores a cero.", parent=self)
            return

        minimo = 2 * h - 1
        if x < minimo:
            messagebox.showwarning("Imposible armar",
                                   f"No es posible armar un árbol de {h} pisos con {x} personas.\n"
                                   f"Con parejas heterosexuales y descendencia, se requieren al menos {minimo} personas (2H−1).",
                                   parent=self)
            return

        # Si supera cierta altura, advertir pero permitir
        if h > 12:
            if not messagebox.askyesno("Advertencia", f"Generar un árbol de {h} pisos puede ser muy alto para la pantalla y dificultar la visualización.\n¿Deseas continuar?", parent=self):
                return

        try:
            self.arbol.generar_arbol_aleatorio(x, h)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el árbol: {str(e)}", parent=self)
            return

        self.destroy()
        self.al_confirmar()


if __name__ == "__main__":
    app = VentanaArbol()
    app.mainloop()
