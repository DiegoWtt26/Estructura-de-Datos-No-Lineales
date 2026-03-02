# Estructura-de-Datos-No-Lineales
# 📚 Parcial: Estructuras de Datos No Lineales
### Ciencias de la Computación e Inteligencia Artificial — Python 3.10+

---

## 📁 Estructura del Proyecto
```
parcial/
├── src/
│   ├── ejercicio1_arbol_nario.py   # Módulo 1 — Árbol N-ario
│   ├── ejercicio2_trie.py          # Módulo 1 — Trie / Autocompletado
│   ├── ejercicio3_hash_table.py    # Módulo 2 — Tabla Hash
│   └── ejercicio4_heap.py          # Módulo 3 — Heap / Priority Queue
├── tests/
│   └── test_parcial.py             # Tests unitarios (unittest)
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos Previos

- **Python 3.10 o superior**
- No se requieren librerías externas (ver `requirements.txt`)

Verificar versión instalada:
```bash
python3 --version
```

---

## 🚀 Cómo Ejecutar

### 1. Clonar o descomprimir el proyecto
```bash
# Opción A — Clonar repositorio
git clone https://github.com/usuario/parcial-no-lineales.git
cd parcial-no-lineales

# Opción B — Descomprimir carpeta
unzip parcial-no-lineales.zip
cd parcial-no-lineales
```

### 2. (Opcional) Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar demos individuales
```bash
# Módulo 1 — Árbol N-ario
python3 src/ejercicio1_arbol_nario.py

# Módulo 1 — Trie / Autocompletado
python3 src/ejercicio2_trie.py

# Módulo 2 — Tabla Hash
python3 src/ejercicio3_hash_table.py

# Módulo 3 — Heap / Priority Queue
python3 src/ejercicio4_heap.py
```

### 5. Ejecutar todos los tests unitarios
```bash
# Con pytest (salida detallada)
python3 -m pytest tests/ -v

# Con unittest estándar
python3 -m unittest discover -s tests -v
```

**Salida esperada de los tests:**
```
tests/test_parcial.py::TestArbolNario::test_buscar_nodo_inexistente_retorna_none  PASSED
tests/test_parcial.py::TestArbolNario::test_iter_recorre_todos_los_nodos          PASSED
...
25 passed in 0.03s
```

---

## 🧩 Descripción de Módulos y Ejercicios

---

### Módulo 1 — Árboles Avanzados

---

#### Ejercicio 1 — `ejercicio1_arbol_nario.py` — Árbol N-ario Organizacional

**Problema:** Modelar la jerarquía universitaria (Rectoría → Facultades → Programas).

**Clases:**
- `OrganizacionNode` — Nodo con `dict[str, OrganizacionNode]` para hijos en O(1).
- `ArbolOrganizacional` — Árbol con inserción, búsqueda y recorridos.

**Características clave:**
- `__iter__` — Itera el árbol directamente con `for nodo in raiz`.
- `recorrer_preorden()` — Generador `yield` para recorrido eficiente en memoria.
- `recorrer_por_nivel()` — BFS implementado también como generador.

---

#### Ejercicio 2 — `ejercicio2_trie.py` — Trie / Autocompletado de Comandos

**Problema:** Autocompletado de comandos técnicos (`git commit`, `docker run`, etc.).

**Clases:**
- `TrieNode` — Nodo con `dict[str, TrieNode]` para aristas.
- `Trie` — Inserción, búsqueda exacta, sugerencias por prefijo y eliminación.

**Características clave:**
- `sugerir(prefijo)` → `Generator[str, None, None]` — Produce sugerencias con `yield`.
- `_dfs_palabras()` — DFS interno como generador para eficiencia de memoria.
- `eliminar()` — Limpieza recursiva de nodos huérfanos tras la eliminación.

---

### Módulo 2 — Tablas Hash

---

#### Ejercicio 3 — `ejercicio3_hash_table.py` — Registro de Estudiantes

**Problema:** Gestionar colisiones en un registro masivo de IDs estudiantiles.

**Clases:**
- `Estudiante` — Dataclass con `id_estudiante`, `nombre`, `programa`, `semestre`.
- `HashTable[V]` — Tabla genérica desde cero, **sin `dict` nativo** en la lógica interna.

**Características clave:**
- `__setitem__` / `__getitem__` — Sintaxis `tabla[id] = estudiante` y `tabla[id]`.
- `__delitem__` / `__contains__` — Soporte para `del tabla[id]` y `id in tabla`.
- Función hash **djb2** para distribución uniforme de claves.
- **Rehashing automático** cuando el factor de carga supera `0.75`.
- **Encadenamiento separado (chaining)** como estrategia de colisión.

---

### Módulo 3 — Montículos (Heaps)

---

#### Ejercicio 4 — `ejercicio4_heap.py` — Planificador de Tareas del Kernel

**Problema:** Simular la cola de prioridad de un sistema operativo (Kernel).

**Clases:**
- `NivelPrioridad` — `IntEnum` con valores `CRITICA=1` … `IDLE=5`.
- `Tarea` — Dataclass con `prioridad`, `nombre`, `timestamp` y `descripcion`.
- `PlanificadorKernel` — Cola de prioridad usando el módulo `heapq`.

**Características clave:**
- `__lt__` — Sobrecarga del operador `<` para que `heapq` ordene objetos `Tarea` automáticamente por prioridad.
- Desempate **FIFO** entre tareas de igual prioridad usando `timestamp`.
- `procesar_todas()` — Generador que extrae y produce todas las tareas en orden.

---

## 📊 Análisis de Complejidad Big O

### Ejercicio 1 — Árbol N-ario

| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| `agregar_hijo(nodo)` | **O(1)** | O(1) | Inserción en `dict` es O(1) amortizado |
| `buscar(nombre)` | **O(n)** | O(h) | DFS visita hasta todos los nodos; pila de recursión = altura h |
| `insertar(padre, hijo)` | **O(n)** | O(h) | Requiere buscar el padre en todo el árbol |
| `__iter__` / `recorrer_preorden()` | **O(n)** | O(h) | Visita cada nodo exactamente una vez; `yield from` evita listas intermedias |
| `recorrer_por_nivel()` BFS | **O(n)** | O(w) | Cola BFS con ancho máximo w |

> `n` = total de nodos · `h` = altura del árbol · `w` = ancho máximo del árbol

---

### Ejercicio 2 — Trie

| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| `insertar(palabra)` | **O(m)** | O(m) | Crea un nodo por cada carácter nuevo |
| `buscar(palabra)` | **O(m)** | O(1) | Recorre exactamente `m` nodos sin recursión |
| `sugerir(prefijo)` | **O(m + k)** | O(h) | Navega el prefijo O(m), luego DFS sobre k resultados |
| `eliminar(palabra)` | **O(m)** | O(m) | Recursión de profundidad igual a la longitud de la palabra |
| Espacio total del Trie | — | **O(N · m)** | N = palabras insertadas · m = longitud promedio |

> `m` = longitud de la cadena · `k` = número de sugerencias encontradas · `N` = total de palabras

---

### Ejercicio 3 — Tabla Hash

| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| `__setitem__` (inserción) | **O(1)** amortizado | O(1) | Hash directo al bucket; rehash ocurre raramente |
| `__getitem__` (búsqueda) | **O(1)** amortizado | O(1) | Bucket en O(1); O(n) solo si todas las claves colisionan |
| `__delitem__` (eliminación) | **O(1)** amortizado | O(1) | Misma lógica que búsqueda |
| `__contains__` | **O(1)** amortizado | O(1) | Verifica el bucket correspondiente |
| `_rehash()` | **O(n)** | O(n) | Redistribuye todos los n elementos; se activa con factor de carga > 0.75 |
| Espacio total | — | **O(n)** | n = pares clave-valor almacenados |

> El peor caso teórico es O(n) si todas las claves producen el mismo hash. La función djb2 y el rehashing automático minimizan esta situación.

---

### Ejercicio 4 — Heap / Priority Queue

| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| `encolar(tarea)` | **O(log n)** | O(1) | `heapq.heappush` restaura el invariante subiendo el nodo |
| `desencolar()` | **O(log n)** | O(1) | `heapq.heappop` reordena el heap bajando el nuevo raíz |
| `ver_siguiente()` | **O(1)** | O(1) | El mínimo siempre está en `_heap[0]` |
| `esta_vacia()` | **O(1)** | O(1) | Evaluación directa del tamaño de la lista |
| `procesar_todas()` generador | **O(n log n)** | O(1) | n extracciones de O(log n); el generador evita lista en memoria |
| Construcción inicial (n tareas) | **O(n)** | O(n) | `heapify` interno es lineal |

---

## 🏆 Resumen de Estándares Aplicados

| Estándar del documento | Implementación |
|---|---|
| **Type Hints — módulo `typing`** | `Dict`, `Optional`, `Generator`, `Iterator`, `List`, `Tuple`, `Generic`, `TypeVar` en todos los archivos |
| **Docstrings Google Style** | Cada clase y método documenta `Args`, `Returns` y `Raises` con tipos explícitos |
| **PEP 8** | `snake_case` en funciones, `PascalCase` en clases, líneas ≤ 88 caracteres, separación de bloques |
| **Generadores `yield`** | `__iter__`, `recorrer_preorden`, `recorrer_por_nivel`, `sugerir`, `_dfs_palabras`, `procesar_todas` |
| **Magic Methods** | `__iter__`, `__setitem__`, `__getitem__`, `__delitem__`, `__contains__`, `__lt__`, `__len__`, `__repr__` |
| **Tests unitarios** | 25 casos en `tests/test_parcial.py` cubriendo casos exitosos y todas las excepciones controladas |
```

---

## 📄 `requirements.txt`
```
# ──────────────────────────────────────────────────────────────────────────────
# Parcial: Estructuras de Datos No Lineales
# Python 3.10+
#
# Este proyecto NO requiere librerías externas.
# Todos los módulos utilizados pertenecen a la librería estándar de Python:
#
#   typing    — Type hints (Dict, Optional, Generator, Iterator, etc.)
#   heapq     — Implementación de min-heap (Ejercicio 4)
#   dataclasses — Decorator @dataclass (Ejercicio 3 y 4)
#   enum      — IntEnum para NivelPrioridad (Ejercicio 4)
#   time      — time.monotonic() para timestamps FIFO (Ejercicio 4)
#   unittest  — Tests unitarios (tests/test_parcial.py)
# ──────────────────────────────────────────────────────────────────────────────

# Dependencia de desarrollo opcional para ejecutar los tests con más detalle:
pytest>=7.4.0
