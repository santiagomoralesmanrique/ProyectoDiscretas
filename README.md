# 🌳 Sistema Interactivo de Árbol Genealógico y Simulación en Grafos

Proyecto desarrollado para la asignatura de **Matemáticas Discretas**.

---

## 📝 Descripción
Un sistema interactivo desarrollado en **Python (Tkinter)** que aplica los fundamentos teóricos de **Matemáticas Discretas (Teoría de Grafos)** para modelar árboles genealógicos como grafos dirigidos acíclicos (DAG), analizar sus propiedades estructurales (matriz de adyacencia, grados de entrada/salida, componentes conexas), calcular caminos de parentesco mediante recorridos BFS, y simular procesos estocásticos de propagación (virus e infecciones con inmunidades personalizadas y herencia genética mendeliana/multifactorial).

El sistema incluye:
- Visualizador gráfico interactivo de árboles y grafos con tarjetas de información y animación paso a paso.
- Ventana de **Modo Educativo** interactivo con 4 pestañas pedagógicas explicativas sobre los algoritmos de grafos aplicados.
- Visualizador interactivo de **Matriz de Adyacencia Dirigida** etiquetada con los nombres de cada persona.
- Simulador epidemiológico y genético con visualización de propagación y panel de estadísticas en tiempo real.
- Generador de árboles genealógicos aleatorios respetando restricciones estructurales y biológicas.

---

## 👥 Integrantes
- **Santiago Morales Manrique**
- **Juan Sebastián Camacho**
- **Diego Alejandro Prieto**

---

## ⚙️ Requisitos
- **Python**: Versión 3.8 o superior.
- **Biblioteca Estándar**: No requiere dependencias de terceros (`pip install` no es necesario). Funciona nativamente con los módulos integrados de Python:
  - `tkinter` (interfaz gráfica de usuario)
  - `math` (cálculos geométricos y de posicionamiento)
  - `random` (simulaciones estocásticas y generación aleatoria)
  - `collections.deque` (colas de procesamiento para recorridos BFS)
  - `unittest` (suite de pruebas automatizadas)

---

## 📦 Instalación
1. Clonar el repositorio o descargar el código fuente:
   ```bash
   git clone https://github.com/santiagomoralesmanrique/ProyectoDiscretas.git
   ```
2. Navegar al directorio raíz del proyecto:
   ```bash
   cd ProyectoDiscretas
   ```

---

## 🚀 Ejecución

### Ejecutar la Aplicación Principal
Para iniciar la interfaz gráfica de usuario (GUI):
```bash
python main.py
```

### Ejecutar las Pruebas Unitarias
Para correr la suite de pruebas unitarias que validan la lógica de grafos y algoritmos:
```bash
python -m unittest test_arbol.py
```

---

## 💡 Ejemplo de Uso
1. **Visualización Inicial**: Al abrir la aplicación (`main.py`), se carga una red familiar predeterminada de 19 personas organizada en 4 generaciones (`datos_prueba.py`) y se dibuja el árbol de manera animada.
2. **Consultar Ficha Técnica**: Haz clic sobre cualquier nodo o tarjeta de persona para abrir un modal con su información detallada: año de nacimiento, estado de vitalidad, reseña biográfica y barras de inmunidad (Gripe, COVID-19, Bacteria).
3. **Búsqueda de Parentesco (BFS)**:
   - Selecciona a **Persona A** y **Persona B** desde las listas desplegables del panel lateral.
   - Haz clic en **"Buscar Parentesco"**. El motor de grafos encontrará la ruta más corta entre ambos nodos e interpretará la relación familiar (ej. *Marta es Madre de Andrés*).
4. **Simulación Epidemiológica (Virus/Contagio)**:
   - Selecciona el tipo de enfermedad (*Gripe*, *COVID-19* o *Infección Bacteriana*).
   - Elige el individuo **Origen de la infección**.
   - Presiona **"Simular Propagación"**. Observa la transmisión del virus nivel a nivel en el grafo y consulta el panel de estadísticas en tiempo real.
5. **Modo Educativo y Matriz de Adyacencia**:
   - Presiona **"Modo Educativo"** en la barra superior para explorar la teoría matemática y el seudocódigo de los algoritmos (DAG, BFS, Epidemiología, Herencia).
   - Haz clic en **"Ver Matriz de Adyacencia"** para examinar la representación matricial dirigida del grafo con los nombres de las personas.

---

## 📌 Estado Actual del Proyecto
- **Estado**: **Completado y Funcional** ✅
- **Funcionalidades Desarrolladas**:
  - [x] Modelado de árbol genealógico como Grafo Dirigido Acíclico (DAG) y verificación DFS de aciclicidad.
  - [x] Algoritmo BFS para cálculo del camino de parentesco más corto y su traducción verbal.
  - [x] Simulador de propagación por niveles con factores de probabilidad base e inmunidad individual.
  - [x] Simulador de herencia genética mendeliana y multifactorial.
  - [x] Generador aleatorio de árboles genealógicos válidos ($X \ge 2H - 1$, diferencia generacional $\ge 17$ años, parejas heterosexuales).
  - [x] Lienzo interactivo en Tkinter con soporte para zoom, desplazamiento (pan) y animaciones de nodos.
  - [x] Panel de estadísticas de propagación en tiempo real con diseño optimizado para alta legibilidad.
  - [x] Visualizador de Matriz de Adyacencia Dirigida con nombres de nodos.
  - [x] Ventana de Modo Educativo con 4 pestañas teóricas sobre los algoritmos empleados.
  - [x] Cobertura de pruebas unitarias automatizadas (`test_arbol.py`) con resultado 100% exitoso (11/11 OK).

---

## 🎯 Núcleo del Proyecto (Conceptos de Matemáticas Discretas)

### 1. Representación de Árboles Genealógicos como Grafos Dirigidos Acíclicos (DAG)
- **Modelado**: Cada persona se representa como un **Nodo** $v \in V$ y cada relación filiativa biológica (padre/madre $\to$ hijo/a) como una **Arista Dirigida** $(u, v) \in E$.
- **Propiedad de DAG**: Se garantiza que el grafo no contenga ciclos dirigidos ($E$ es acíclico), representando la irreversibilidad temporal de la descendencia biológica. La verificación se realiza computacionalmente mediante **DFS con coloreado de 3 estados** (Blanco, Gris, Negro).

### 2. Algoritmos de Recorrido para Búsqueda de Parentesco (BFS)
- **Búsqueda de Caminos**: Se implementa un recorrido en anchura **BFS (Breadth-First Search)** en el grafo no dirigido subyacente para encontrar la ruta más corta entre dos individuos $A$ y $B$.
- **Traducción de Relaciones Binarias**: La secuencia de pasos dirigidos (`UP` hacia progenitores, `DOWN` hacia descendientes, `SPOUSE` hacia pareja) se traduce formalmente a términos de parentesco en español (*Abuelo/a*, *Tío/a*, *Sobrino/a*, *Primo/a hermano/a*, etc.).

### 3. Simulador de Propagación en Redes y Grafos
- **Simulación Epidemiológica (Virus / Contagio)**: Algoritmo de propagación por niveles (BFS) donde la probabilidad de contagio en cada receptor $v$ depende de la probabilidad base de la enfermedad $P_{base}$ y la inmunidad específica del individuo $I_v$:
  $$P_{\text{contagio}}(v) = P_{\text{base}} \times (1 - I_v)$$
  Se modelan inmunidades específicas para **Gripe**, **COVID-19** e **Infección Bacteriana**.
- **Herencia Genética y Multifactorial**: Modelado de herencia mendeliana (alelos $A/a$) y simulación multifactorial con atenuación exponencial según la distancia generacional $d$:
  $$P_{\text{herencia}}(d) = P_{\text{base}} \times 0.5^d$$

### 4. Conectividad y Propiedades Estructurales
- **Conectividad**: Verificación de si la red familiar es un único grafo conexo o un bosque (múltiples componentes conexas) mediante exploración BFS.
- **Grados de Nodos**: Cálculo del grado de entrada ($\text{deg}^-$: padres), grado de salida ($\text{deg}^+$: hijos) y grado total ($\text{deg}$: relaciones totales).

---

## 🔬 Caso de Prueba Manual Validado (Paso a Paso)

Para validar la precisión del simulador de propagación epidemiológica, se presenta la siguiente verificación manual en un subárbol reducido de 5 personas:

### Configuración del Grafo de Prueba
- **Nodos ($V$)**:
  - $p_1$ (Efraín, n. 1931, $I_{\text{gripe}} = 0.15$) — *Origen del virus*
  - $p_2$ (Rosario, n. 1934, $I_{\text{gripe}} = 0.20$) — *Pareja de $p_1$*
  - $p_3$ (Marta, n. 1958, $I_{\text{gripe}} = 0.40$) — *Hija de $p_1$ y $p_2$*
  - $p_4$ (Héctor, n. 1956, $I_{\text{gripe}} = 0.45$) — *Pareja de $p_3$*
  - $p_5$ (Andrés, n. 1984, $I_{\text{gripe}} = 0.65$) — *Hijo de $p_3$ y $p_4$*

### Parámetros de Prueba
- **Enfermedad**: Gripe ($P_{\text{base}} = 0.80$)
- **Nodo Origen**: $p_1$ (Infectado en Ronda 0)

### Simulación Paso a Paso (Cálculo Manual vs Software)

1. **Ronda 0 (Origen)**:
   - Infectados: $\{p_1\}$
   - Estado: $p_1$ marcado como `☣️ INFECTADO`.

2. **Ronda 1 (Vecinos de $p_1$ $\to$ $\{p_2, p_3\}$)**:
   - **Evaluación a $p_2$ (Rosario)**:
     $$P(p_2) = P_{\text{base}} \times (1 - I_{\text{gripe}}(p_2)) = 0.80 \times (1 - 0.20) = 0.80 \times 0.80 = 0.64 \text{ (64% de probabilidad)}$$
   - **Evaluación a $p_3$ (Marta)**:
     $$P(p_3) = P_{\text{base}} \times (1 - I_{\text{gripe}}(p_3)) = 0.80 \times (1 - 0.40) = 0.80 \times 0.60 = 0.48 \text{ (48% de probabilidad)}$$

3. **Ronda 2 (Si $p_3$ se infecta, vecinos de $p_3$ $\to$ $\{p_4, p_5\}$)**:
   - **Evaluación a $p_4$ (Héctor)**:
     $$P(p_4) = 0.80 \times (1 - 0.45) = 0.80 \times 0.55 = 0.44 \text{ (44%)}$$
   - **Evaluación a $p_5$ (Andrés)**:
     $$P(p_5) = 0.80 \times (1 - 0.65) = 0.80 \times 0.35 = 0.28 \text{ (28%)}$$

> **Resultado**: El algoritmo BFS en `arbol.py` implementa exactamente esta lógica estocástica paso a paso, confirmando la validez del modelo.

---

## 🛠️ Estructura del Código

```text
ProyectoDiscretas/
│
├── docs/
│   └── IdeaProyecto.pdf # Documento de propuesta del proyecto
├── nodo.py          # Clase Nodo (unidad básica con género, nacimiento e inmunidades)
├── arbol.py         # Motor de Grafo (BFS, DFS, validación DAG, conectividad y simulaciones)
├── datos_prueba.py  # Base de datos ficticia de 19 personas en 4 generaciones
├── main.py          # Interfaz gráfica de usuario (GUI Tkinter con animación y modo educativo)
├── test_arbol.py    # Suite de pruebas unitarias automatizadas (11/11 OK)
└── README.md        # Documentación principal del proyecto
```
