# 🌳 Sistema Interactivo de Árbol Genealógico y Simulación en Grafos

Un proyecto de software interactivo desarrollado en **Python (Tkinter)** que aplica los fundamentos teóricos de **Matemáticas Discretas II (Teoría de Grafos)** para modelar árboles genealógicos como grafos, analizar sus propiedades estructurales, calcular caminos de parentesco mediante recorridos de grafos y simular procesos de propagación de características (apellidos, enfermedades virales e inmunidad, y herencia genética).

---

## 🎯 Núcleo del Proyecto (Conceptos de Matemáticas Discretas)

Siguiendo las recomendaciones pedagógicas del curso, el proyecto centra su arquitectura en **4 pilares fundamentales de Teoría de Grafos**:

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

## 💻 Características del Sistema

- **Visualizador Gráfico Interactivo (`main.py`)**: Interfaz desarrollada en Tkinter con lienzo `Canvas` responsivo, animaciones por capas generación por generación y curvas de Bézier cúbicas para las ramas familiares.
- **Base de Datos Familiar (`datos_prueba.py`)**: Registros de 19 personas organizadas en 4 generaciones con parejas heterosexuales, género, años de nacimiento e inmunidades.
- **Generador de Árboles Aleatorios**: Genera grafos aleatorios válidos dados $X$ personas y $H$ pisos/generaciones, haciendo cumplir las siguientes restricciones matemáticas:
  1. $X \ge 2H - 1$ (mínimo 2 personas por piso para formar parejas con descendencia, 1 en el último piso).
  2. Parejas heterosexuales exclusivas para procreación.
  3. Diferencia mínima de año de nacimiento $\ge 17$ años entre padres e hijos.
  4. Cero huérfanos solteros (todo hijo posee 2 padres acoplados).
- **Ficha Médica y Biográfica**: Modal al hacer clic sobre cualquier tarjeta que muestra año de nacimiento, indicador de vitalidad (`✝ Fallecido` si nació antes de 1941), barras de inmunidad y reseña biográfica.

---

## 🛠️ Estructura del Código

```text
ProyectoDiscretas/
│
├── nodo.py          # Clase Nodo (unidad básica con género, nacimiento e inmunidades)
├── arbol.py         # Motor de Grafo (BFS, DFS, validación DAG, conectividad y simulaciones)
├── datos_prueba.py  # Base de datos ficticia de 19 personas en 4 generaciones
├── main.py          # Interfaz gráfica de usuario (GUI Tkinter)
├── test_arbol.py    # Suite de pruebas unitarias automatizadas (11/11 OK)
└── README.md        # Documentación principal del proyecto
```

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior (incluye `tkinter` y `unittest` en la biblioteca estándar).

### Ejecutar la Aplicación
```bash
python main.py
```

### Ejecutar las Pruebas Unitarias
```bash
python -m unittest test_arbol.py
```

---

## 🧪 Pruebas Automatizadas

El proyecto cuenta con una suite completa de pruebas unitarias en `test_arbol.py` que verifican:
- Asignación correcta de atributos de `Nodo` (género, nacimiento, inmunidades).
- Detección de ciclos en grafos (DAG) y conectividad de componentes.
- Búsqueda exacta de caminos BFS y traducción de parentesco.
- Inmunidades específicas por tipo de enfermedad (Gripe, COVID-19, Bacteria).
- Restricciones del generador aleatorio ($X \ge 2H - 1$ y diferencia de edad $\ge 17$).

---

## 👨‍💻 Autores
- Proyecto desarrollado para la asignatura **Matemáticas Discretas II**.
