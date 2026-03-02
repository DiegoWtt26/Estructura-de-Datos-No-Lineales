"""
Ejercicio 3: Registro de Estudiantes (Hash Table)
Módulo 2: Tablas Hash

Implementa una tabla hash desde cero con manejo de colisiones
por encadenamiento (separate chaining) y rehashing automático.
No se utiliza dict nativo para la lógica interna de almacenamiento.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Iterator, List, Optional, Tuple, TypeVar

V = TypeVar("V")


@dataclass
class Estudiante:
    """Representa un estudiante en el sistema de registro universitario.

    Attributes:
        id_estudiante (str): Código único del estudiante.
        nombre (str): Nombre completo del estudiante.
        programa (str): Nombre del programa académico.
        semestre (int): Semestre actual del estudiante.

    Example:
        >>> est = Estudiante("20231001", "Ana García", "Sistemas", 4)
        >>> print(est)
        Estudiante(id='20231001', nombre='Ana García', programa='Sistemas', semestre=4)
    """

    id_estudiante: str
    nombre: str
    programa: str
    semestre: int = 1

    def __repr__(self) -> str:
        """Devuelve representación legible del estudiante.

        Returns:
            str: Cadena con todos los atributos del estudiante.
        """
        return (
            f"Estudiante(id='{self.id_estudiante}', nombre='{self.nombre}', "
            f"programa='{self.programa}', semestre={self.semestre})"
        )


class HashTable(Generic[V]):
    """Tabla Hash genérica con encadenamiento para manejo de colisiones.

    Implementa los métodos mágicos __setitem__ y __getitem__ para que
    la tabla sea usable con la sintaxis nativa tabla[clave] = valor.

    El rehashing se activa automáticamente cuando el factor de carga
    supera _FACTOR_CARGA_MAX, duplicando la capacidad.

    **No se utiliza dict nativo para almacenar los pares clave-valor.**

    Attributes:
        capacidad (int): Número actual de buckets.
        tamanio (int): Cantidad de pares clave-valor almacenados.
        _tabla (List[List[Tuple[str, V]]]): Arreglo de listas (chaining).

    Complexity:
        Inserción:   O(1) amortizado.
        Búsqueda:    O(1) amortizado, O(n) peor caso (colisiones).
        Eliminación: O(1) amortizado.
        Rehash:      O(n) — ocurre raramente.

    Example:
        >>> tabla: HashTable[Estudiante] = HashTable()
        >>> tabla["E001"] = Estudiante("E001", "Ana", "Sistemas", 3)
        >>> tabla["E001"]
        Estudiante(id='E001', ...)
    """

    _FACTOR_CARGA_MAX: float = 0.75
    _CAPACIDAD_INICIAL: int = 16

    def __init__(self, capacidad: int = _CAPACIDAD_INICIAL) -> None:
        """Inicializa la tabla hash con una capacidad inicial dada.

        Args:
            capacidad (int): Número inicial de buckets. Se recomienda
                usar potencias de 2. Por defecto 16.

        Raises:
            ValueError: Si la capacidad proporcionada es menor a 1.

        Example:
            >>> tabla: HashTable[str] = HashTable(capacidad=32)
        """
        if capacidad < 1:
            raise ValueError(
                f"La capacidad debe ser mayor a 0, se recibió: {capacidad}."
            )
        self.capacidad: int = capacidad
        self.tamanio: int = 0
        self._tabla: List[List[Tuple[str, V]]] = [
            [] for _ in range(self.capacidad)
        ]

    # ── Hashing ──────────────────────────────────────────────────────────────

    def _calcular_hash(self, clave: str, capacidad: Optional[int] = None) -> int:
        """Calcula el índice del bucket para una clave (algoritmo djb2).

        Args:
            clave (str): Clave a hashear.
            capacidad (Optional[int]): Capacidad a usar para el módulo.
                Si es None, usa self.capacidad.

        Returns:
            int: Índice del bucket en el rango [0, capacidad).
        """
        cap: int = capacidad if capacidad is not None else self.capacidad
        valor_hash: int = 5381
        for caracter in clave:
            valor_hash = (valor_hash * 33) ^ ord(caracter)
        return valor_hash % cap

    # ── Rehashing ────────────────────────────────────────────────────────────

    def _rehash(self) -> None:
        """Duplica la capacidad y redistribuye todos los pares existentes.

        Se invoca automáticamente desde __setitem__ cuando el factor de
        carga supera _FACTOR_CARGA_MAX. Garantiza que las búsquedas
        futuras continúen siendo O(1) amortizado.
        """
        nueva_capacidad: int = self.capacidad * 2
        nueva_tabla: List[List[Tuple[str, V]]] = [
            [] for _ in range(nueva_capacidad)
        ]
        for bucket in self._tabla:
            for clave, valor in bucket:
                nuevo_indice: int = self._calcular_hash(clave, nueva_capacidad)
                nueva_tabla[nuevo_indice].append((clave, valor))
        self.capacidad = nueva_capacidad
        self._tabla = nueva_tabla

    # ── Métodos Mágicos (Componente Pro) ─────────────────────────────────────

    def __setitem__(self, clave: str, valor: V) -> None:
        """Inserta o actualiza un valor usando la sintaxis tabla[clave] = valor.

        Si el factor de carga supera el umbral, realiza rehash antes de insertar.
        Si la clave ya existe, actualiza el valor en su lugar.

        Args:
            clave (str): Clave de identificación (ej. ID del estudiante).
            valor (V): Objeto a almacenar asociado a la clave.

        Example:
            >>> tabla["20231001"] = Estudiante("20231001", "Ana", "Sistemas", 2)
        """
        if self.tamanio / self.capacidad >= self._FACTOR_CARGA_MAX:
            self._rehash()

        indice: int = self._calcular_hash(clave)
        bucket: List[Tuple[str, V]] = self._tabla[indice]

        for i, (k, _) in enumerate(bucket):
            if k == clave:
                bucket[i] = (clave, valor)
                return

        bucket.append((clave, valor))
        self.tamanio += 1

    def __getitem__(self, clave: str) -> V:
        """Obtiene el valor asociado a una clave con la sintaxis tabla[clave].

        Args:
            clave (str): Clave a buscar en la tabla.

        Returns:
            V: El valor almacenado bajo esa clave.

        Raises:
            KeyError: Si la clave no existe en la tabla hash.

        Example:
            >>> estudiante = tabla["20231001"]
        """
        indice: int = self._calcular_hash(clave)
        for k, v in self._tabla[indice]:
            if k == clave:
                return v
        raise KeyError(f"La clave '{clave}' no fue encontrada en la tabla hash.")

    def __delitem__(self, clave: str) -> None:
        """Elimina un par clave-valor con la sintaxis del tabla[clave].

        Args:
            clave (str): Clave del elemento a eliminar.

        Raises:
            KeyError: Si la clave no existe en la tabla.

        Example:
            >>> del tabla["20231001"]
        """
        indice: int = self._calcular_hash(clave)
        bucket: List[Tuple[str, V]] = self._tabla[indice]
        for i, (k, _) in enumerate(bucket):
            if k == clave:
                bucket.pop(i)
                self.tamanio -= 1
                return
        raise KeyError(f"La clave '{clave}' no fue encontrada en la tabla hash.")

    def __contains__(self, clave: str) -> bool:
        """Verifica si una clave existe usando el operador in.

        Args:
            clave (str): Clave a verificar.

        Returns:
            bool: True si la clave existe, False en caso contrario.

        Example:
            >>> "20231001" in tabla
            True
        """
        indice: int = self._calcular_hash(clave)
        return any(k == clave for k, _ in self._tabla[indice])

    def __len__(self) -> int:
        """Retorna el número de pares clave-valor almacenados.

        Returns:
            int: Cantidad de elementos en la tabla.

        Example:
            >>> len(tabla)
            5
        """
        return self.tamanio

    def __iter__(self) -> Iterator[str]:
        """Itera sobre todas las claves almacenadas en la tabla.

        Yields:
            str: Cada clave en el orden de los buckets.

        Example:
            >>> for clave in tabla:
            ...     print(clave)
        """
        for bucket in self._tabla:
            for clave, _ in bucket:
                yield clave

    def __repr__(self) -> str:
        """Devuelve representación legible de la tabla.

        Returns:
            str: Cadena con capacidad, tamaño y factor de carga.
        """
        return (
            f"HashTable(capacidad={self.capacidad}, "
            f"tamanio={self.tamanio}, "
            f"factor_carga={self.factor_carga():.2f})"
        )

    # ── Métodos Auxiliares ───────────────────────────────────────────────────

    def factor_carga(self) -> float:
        """Calcula el factor de carga actual de la tabla.

        Returns:
            float: Cociente tamanio / capacidad.

        Example:
            >>> tabla.factor_carga()
            0.31
        """
        return self.tamanio / self.capacidad

    def obtener(self, clave: str, por_defecto: Any = None) -> Any:
        """Retorna el valor de una clave o un valor por defecto si no existe.

        Args:
            clave (str): Clave a buscar.
            por_defecto (Any): Valor a retornar si la clave no existe.

        Returns:
            Any: El valor almacenado o por_defecto si la clave no existe.

        Example:
            >>> tabla.obtener("99999", None)
            None
        """
        try:
            return self[clave]
        except KeyError:
            return por_defecto


# ─── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    registro: HashTable[Estudiante] = HashTable()

    registro["20231001"] = Estudiante("20231001", "Ana García",   "Sistemas",  4)
    registro["20231002"] = Estudiante("20231002", "Luis Torres",  "Civil",     2)
    registro["20231003"] = Estudiante("20231003", "María López",  "Biología",  6)
    registro["20231004"] = Estudiante("20231004", "Carlos Ruiz",  "Física",    3)
    registro["20231005"] = Estudiante("20231005", "Sofía Mora",   "Sistemas",  5)

    print("=== Registro de Estudiantes ===")
    print(registro)
    print(f"\nBuscar '20231001': {registro['20231001']}")
    print(f"¿Existe '20231002'?: {'20231002' in registro}")
    print(f"¿Existe '99999999'?: {'99999999' in registro}")

    print("\nTodos los registrados:")
    for clave in registro:
        print(f"  {clave} → {registro[clave].nombre}")

    del registro["20231002"]
    print(f"\nTras eliminar '20231002': {len(registro)} estudiantes")

    try:
        _ = registro["99999999"]
    except KeyError as exc:
        print(f"KeyError controlado: {exc}")