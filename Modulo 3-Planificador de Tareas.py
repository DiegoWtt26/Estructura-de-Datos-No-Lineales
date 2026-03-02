"""
Ejercicio 4: Planificador de Tareas (Priority Queue)
Módulo 3: Montículos (Heaps)

Simula la cola de prioridad de un Kernel usando heapq.
La clase Tarea sobrecarga __lt__ para que heapq ordene automáticamente
por prioridad y timestamp (desempate FIFO).
"""

from __future__ import annotations

import heapq
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Generator, List, Optional


class NivelPrioridad(IntEnum):
    """Niveles de prioridad para tareas del Kernel del sistema operativo.

    Los valores numéricos menores indican mayor prioridad, lo que es
    compatible con el comportamiento de min-heap de heapq.

    Attributes:
        CRITICA (int): Prioridad más alta, para interrupciones críticas.
        ALTA (int): Tareas de alta prioridad como gestión de memoria.
        MEDIA (int): Actualizaciones y procesos regulares.
        BAJA (int): Mantenimiento y tareas diferibles.
        IDLE (int): Tareas de fondo sin urgencia.
    """

    CRITICA = 1
    ALTA = 2
    MEDIA = 3
    BAJA = 4
    IDLE = 5


@dataclass
class Tarea:
    """Representa una tarea en la cola de prioridad del Kernel.

    Diseñada para ser usada directamente con heapq. El operador __lt__
    está sobrecargado para que heapq pueda comparar objetos Tarea y
    ordenarlos automáticamente por prioridad y timestamp.

    Attributes:
        prioridad (NivelPrioridad): Nivel de prioridad de la tarea.
        nombre (str): Nombre identificador de la tarea.
        timestamp (float): Tiempo de creación (para desempate FIFO).
        descripcion (Optional[str]): Descripción detallada de la tarea.

    Example:
        >>> tarea = Tarea(NivelPrioridad.CRITICA, "kernel panic handler")
        >>> tarea.prioridad
        NivelPrioridad.CRITICA
    """

    prioridad: NivelPrioridad
    nombre: str
    timestamp: float = field(default_factory=time.monotonic)
    descripcion: Optional[str] = None

    def __lt__(self, otra: Tarea) -> bool:
        """Sobrecarga del operador < para ordenamiento automático en heapq.

        heapq requiere que los elementos sean comparables. Este método
        permite que heapq ordene objetos Tarea sin configuración adicional.

        Criterio de ordenamiento:
          1. Primero por prioridad (menor valor = mayor prioridad).
          2. En caso de empate, por timestamp (FIFO: primero en llegar).

        Args:
            otra (Tarea): Tarea con la que se compara la actual.

        Returns:
            bool: True si esta tarea debe ejecutarse antes que 'otra'.

        Example:
            >>> t1 = Tarea(NivelPrioridad.CRITICA, "T1")
            >>> t2 = Tarea(NivelPrioridad.BAJA, "T2")
            >>> t1 < t2
            True
        """
        if self.prioridad != otra.prioridad:
            return int(self.prioridad) < int(otra.prioridad)
        return self.timestamp < otra.timestamp

    def __repr__(self) -> str:
        """Devuelve representación legible de la tarea.

        Returns:
            str: Cadena con nombre y nivel de prioridad.
        """
        return (
            f"Tarea(nombre='{self.nombre}', "
            f"prioridad={self.prioridad.name})"
        )


class PlanificadorKernel:
    """Cola de prioridad que simula el planificador de tareas de un Kernel.

    Usa el módulo heapq para mantener el invariante de min-heap, garantizando
    O(log n) en inserción y extracción. La prioridad real la determina el
    método __lt__ de la clase Tarea.

    Attributes:
        _heap (List[Tarea]): Lista interna gestionada por heapq.
        _tareas_procesadas (int): Contador histórico de tareas ejecutadas.

    Complexity:
        encolar:       O(log n)
        desencolar:    O(log n)
        ver_siguiente: O(1)
        esta_vacia:    O(1)

    Example:
        >>> planificador = PlanificadorKernel()
        >>> planificador.encolar(Tarea(NivelPrioridad.ALTA, "Limpiar memoria"))
        >>> planificador.desencolar()
        Tarea(nombre='Limpiar memoria', prioridad=ALTA)
    """

    def __init__(self) -> None:
        """Inicializa el planificador con una cola vacía."""
        self._heap: List[Tarea] = []
        self._tareas_procesadas: int = 0

    def encolar(self, tarea: Tarea) -> None:
        """Agrega una tarea a la cola de prioridad.

        Args:
            tarea (Tarea): Tarea a encolar. Su posición en la cola
                se determina automáticamente por Tarea.__lt__.

        Raises:
            TypeError: Si el argumento no es una instancia de Tarea.

        Example:
            >>> planificador.encolar(Tarea(NivelPrioridad.CRITICA, "IRQ handler"))
        """
        if not isinstance(tarea, Tarea):
            raise TypeError(
                f"Se esperaba un objeto Tarea, se recibió: {type(tarea).__name__}."
            )
        heapq.heappush(self._heap, tarea)

    def desencolar(self) -> Tarea:
        """Extrae y retorna la tarea de mayor prioridad de la cola.

        Args:
            No recibe argumentos.

        Returns:
            Tarea: La tarea con el mayor nivel de prioridad (y más antigua
                en caso de empate de prioridad).

        Raises:
            IndexError: Si la cola está vacía al momento de llamar.

        Example:
            >>> siguiente = planificador.desencolar()
            >>> print(siguiente.nombre)
        """
        if not self._heap:
            raise IndexError(
                "No se puede desencolar: el planificador de tareas está vacío."
            )
        tarea: Tarea = heapq.heappop(self._heap)
        self._tareas_procesadas += 1
        return tarea

    def ver_siguiente(self) -> Optional[Tarea]:
        """Consulta la tarea de mayor prioridad sin extraerla de la cola.

        Args:
            No recibe argumentos.

        Returns:
            Optional[Tarea]: La tarea con mayor prioridad,
                o None si la cola está vacía.

        Example:
            >>> tarea = planificador.ver_siguiente()
        """
        return self._heap[0] if self._heap else None

    def procesar_todas(self) -> Generator[Tarea, None, None]:
        """Extrae y genera todas las tareas en orden de prioridad.

        Usa yield para procesar las tareas una a una sin cargar
        toda la cola en memoria simultáneamente.

        Yields:
            Tarea: Cada tarea en orden de prioridad descendente.

        Example:
            >>> for tarea in planificador.procesar_todas():
            ...     ejecutar(tarea)
        """
        while not self.esta_vacia():
            yield self.desencolar()

    def esta_vacia(self) -> bool:
        """Indica si la cola de tareas está vacía.

        Returns:
            bool: True si no hay tareas pendientes, False en caso contrario.

        Example:
            >>> planificador.esta_vacia()
            False
        """
        return len(self._heap) == 0

    def __len__(self) -> int:
        """Retorna el número de tareas pendientes en la cola.

        Returns:
            int: Cantidad de tareas aún no procesadas.

        Example:
            >>> len(planificador)
            3
        """
        return len(self._heap)

    def __repr__(self) -> str:
        """Devuelve representación legible del planificador.

        Returns:
            str: Cadena con tareas pendientes y procesadas.
        """
        return (
            f"PlanificadorKernel(pendientes={len(self)}, "
            f"procesadas={self._tareas_procesadas})"
        )


# ─── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    planificador = PlanificadorKernel()

    planificador.encolar(Tarea(NivelPrioridad.BAJA,    "Desfragmentar disco",
                               descripcion="Mantenimiento preventivo"))
    planificador.encolar(Tarea(NivelPrioridad.CRITICA, "Kernel panic handler",
                               descripcion="Gestión de errores críticos"))
    planificador.encolar(Tarea(NivelPrioridad.MEDIA,   "Actualizar drivers",
                               descripcion="Periféricos USB"))
    planificador.encolar(Tarea(NivelPrioridad.ALTA,    "Gestión de memoria",
                               descripcion="Liberar páginas huérfanas"))
    planificador.encolar(Tarea(NivelPrioridad.CRITICA, "Interrupción hardware",
                               descripcion="IRQ 14 — Disco primario"))
    planificador.encolar(Tarea(NivelPrioridad.IDLE,    "Estadísticas del sistema"))

    print("=== Planificador de Tareas del Kernel ===")
    print(planificador)
    print(f"Siguiente tarea: {planificador.ver_siguiente()}\n")

    print("=== Ejecución por orden de prioridad (generador) ===")
    for orden, tarea in enumerate(planificador.procesar_todas(), start=1):
        print(f"  [{orden}] {tarea.prioridad.name:8} | {tarea.nombre}")

    print(f"\n{planificador}")