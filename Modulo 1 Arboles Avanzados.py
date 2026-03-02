"""
Ejercicio 1: Estructura Organizacional (Árbol N-ario)
Módulo 1: Árboles Avanzados

Modela la jerarquía universitaria: Rectoría → Facultades → Programas.
"""

from __future__ import annotations

from typing import Dict, Generator, Iterator, Optional


class OrganizacionNode:
    """Nodo de un árbol N-ario para representar unidades organizacionales.

    Cada nodo almacena sus hijos en un diccionario para garantizar
    acceso, inserción y búsqueda directa en O(1) por nombre.

    Attributes:
        nombre (str): Nombre de la unidad organizacional.
        hijos (Dict[str, OrganizacionNode]): Hijos indexados por nombre.

    Example:
        >>> nodo = OrganizacionNode("Rectoría")
        >>> nodo.agregar_hijo(OrganizacionNode("Facultad de Ingeniería"))
    """

    def __init__(self, nombre: str) -> None:
        """Inicializa un nodo con nombre y sin hijos.

        Args:
            nombre (str): Nombre de la unidad organizacional.
        """
        self.nombre: str = nombre
        self.hijos: Dict[str, OrganizacionNode] = {}

    def agregar_hijo(self, nodo: OrganizacionNode) -> None:
        """Agrega un nodo hijo al nodo actual.

        Args:
            nodo (OrganizacionNode): Nodo hijo a agregar.

        Raises:
            ValueError: Si ya existe un hijo con el mismo nombre.

        Example:
            >>> padre = OrganizacionNode("Rectoría")
            >>> padre.agregar_hijo(OrganizacionNode("Facultad"))
        """
        if nodo.nombre in self.hijos:
            raise ValueError(
                f"Ya existe un nodo hijo con el nombre '{nodo.nombre}'."
            )
        self.hijos[nodo.nombre] = nodo

    def buscar(self, nombre: str) -> Optional[OrganizacionNode]:
        """Busca un nodo por nombre usando recorrido DFS recursivo.

        Args:
            nombre (str): Nombre del nodo a buscar.

        Returns:
            Optional[OrganizacionNode]: El nodo encontrado,
                o None si no existe en el subárbol.

        Example:
            >>> raiz = OrganizacionNode("Rectoría")
            >>> raiz.buscar("Rectoría")
            OrganizacionNode(nombre='Rectoría')
        """
        if self.nombre == nombre:
            return self
        for hijo in self.hijos.values():
            resultado: Optional[OrganizacionNode] = hijo.buscar(nombre)
            if resultado is not None:
                return resultado
        return None

    def __iter__(self) -> Iterator[OrganizacionNode]:
        """Permite iterar el subárbol en preorden con un bucle for.

        Implementa el método mágico __iter__ para que cada instancia
        sea directamente iterable, recorriendo en preorden (raíz primero).

        Yields:
            OrganizacionNode: Cada nodo del árbol en preorden (DFS).

        Example:
            >>> for nodo in raiz:
            ...     print(nodo.nombre)
        """
        yield self
        for hijo in self.hijos.values():
            yield from hijo

    def __repr__(self) -> str:
        """Devuelve representación legible del nodo.

        Returns:
            str: Cadena con nombre e hijos directos del nodo.
        """
        return (
            f"OrganizacionNode(nombre='{self.nombre}', "
            f"hijos={list(self.hijos.keys())})"
        )


class ArbolOrganizacional:
    """Árbol N-ario que modela la jerarquía universitaria completa.

    Permite insertar unidades, buscarlas y recorrerlas de forma
    eficiente usando generadores para minimizar el uso de memoria.

    Attributes:
        raiz (OrganizacionNode): Nodo raíz del árbol (ej. Rectoría).

    Example:
        >>> arbol = ArbolOrganizacional("Rectoría")
        >>> arbol.insertar("Rectoría", "Facultad de Ingeniería")
    """

    def __init__(self, nombre_raiz: str) -> None:
        """Inicializa el árbol con un único nodo raíz.

        Args:
            nombre_raiz (str): Nombre del nodo raíz del árbol.
        """
        self.raiz: OrganizacionNode = OrganizacionNode(nombre_raiz)

    def insertar(self, nombre_padre: str, nombre_hijo: str) -> None:
        """Inserta un nuevo nodo como hijo de un nodo existente.

        Args:
            nombre_padre (str): Nombre del nodo padre destino.
            nombre_hijo (str): Nombre del nuevo nodo hijo.

        Raises:
            KeyError: Si el nodo padre no existe en el árbol.
            ValueError: Si ya existe un hijo con ese nombre bajo el padre.

        Example:
            >>> arbol.insertar("Rectoría", "Facultad de Ciencias")
        """
        nodo_padre: Optional[OrganizacionNode] = self.raiz.buscar(nombre_padre)
        if nodo_padre is None:
            raise KeyError(
                f"El nodo padre '{nombre_padre}' no existe en el árbol."
            )
        nodo_padre.agregar_hijo(OrganizacionNode(nombre_hijo))

    def recorrer_preorden(self) -> Generator[str, None, None]:
        """Recorre todo el árbol en preorden generando nombres de nodos.

        Usa yield para un recorrido eficiente en memoria, apto para
        árboles de gran tamaño sin cargar todos los nodos en RAM.

        Yields:
            str: Nombre de cada nodo visitado en preorden.

        Example:
            >>> for nombre in arbol.recorrer_preorden():
            ...     print(nombre)
        """
        for nodo in self.raiz:
            yield nodo.nombre

    def recorrer_por_nivel(self) -> Generator[OrganizacionNode, None, None]:
        """Recorre el árbol nivel por nivel (BFS) usando un generador.

        Implementa BFS con una cola explícita. Usa yield para eficiencia
        de memoria en árboles con miles de nodos.

        Yields:
            OrganizacionNode: Cada nodo visitado nivel por nivel.

        Example:
            >>> for nodo in arbol.recorrer_por_nivel():
            ...     print(nodo.nombre)
        """
        cola: list[OrganizacionNode] = [self.raiz]
        while cola:
            nodo_actual: OrganizacionNode = cola.pop(0)
            yield nodo_actual
            cola.extend(nodo_actual.hijos.values())

    def mostrar_jerarquia(
        self,
        nodo: Optional[OrganizacionNode] = None,
        nivel: int = 0,
    ) -> None:
        """Imprime la jerarquía del árbol con indentación visual.

        Args:
            nodo (Optional[OrganizacionNode]): Nodo desde donde imprimir.
                Si es None, comienza desde la raíz.
            nivel (int): Nivel de profundidad actual (controla indentación).
        """
        if nodo is None:
            nodo = self.raiz
        prefijo: str = "  " * nivel + ("└─ " if nivel > 0 else "")
        print(f"{prefijo}{nodo.nombre}")
        for hijo in nodo.hijos.values():
            self.mostrar_jerarquia(hijo, nivel + 1)


# ─── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    arbol = ArbolOrganizacional("Rectoría")
    arbol.insertar("Rectoría", "Facultad de Ingeniería")
    arbol.insertar("Rectoría", "Facultad de Ciencias")
    arbol.insertar("Rectoría", "Facultad de Humanidades")
    arbol.insertar("Facultad de Ingeniería", "Programa de Sistemas")
    arbol.insertar("Facultad de Ingeniería", "Programa de Civil")
    arbol.insertar("Facultad de Ciencias", "Programa de Biología")
    arbol.insertar("Facultad de Ciencias", "Programa de Física")

    print("=== Jerarquía Universitaria ===")
    arbol.mostrar_jerarquia()

    print("\n=== Iteración directa con __iter__ (Componente Pro) ===")
    for nodo in arbol.raiz:
        print(f"  • {nodo.nombre}")

    print("\n=== Recorrido preorden con generador (Gestión de Memoria) ===")
    for nombre in arbol.recorrer_preorden():
        print(f"  → {nombre}")

    print("\n=== Recorrido por nivel BFS ===")
    for nodo in arbol.recorrer_por_nivel():
        print(f"  ○ {nodo.nombre}")