"""
Ejercicio 2: Diccionario Técnico (Trie)
Módulo 1: Árboles Avanzados

Implementa un sistema de autocompletado de comandos técnicos
usando una estructura Trie con generadores para eficiencia de memoria.
"""

from __future__ import annotations

from typing import Dict, Generator, Optional


class TrieNode:
    """Nodo interno de la estructura Trie.

    Cada nodo representa un carácter en el camino hacia una palabra completa.
    Los hijos se almacenan en un diccionario para acceso O(1) por carácter.

    Attributes:
        hijos (Dict[str, TrieNode]): Mapa de carácter → nodo hijo.
        es_fin (bool): True si este nodo marca el final de una palabra válida.
        palabra_completa (Optional[str]): La palabra completa almacenada al
            final del camino, o None si no es un nodo terminal.

    Example:
        >>> nodo = TrieNode()
        >>> nodo.es_fin
        False
    """

    def __init__(self) -> None:
        """Inicializa un nodo Trie sin hijos y sin ser terminal."""
        self.hijos: Dict[str, TrieNode] = {}
        self.es_fin: bool = False
        self.palabra_completa: Optional[str] = None


class Trie:
    """Estructura Trie para autocompletado eficiente de comandos técnicos.

    Permite insertar palabras o comandos y recuperar sugerencias a partir
    de un prefijo dado. El método sugerir usa yield (generador) para
    eficiencia de memoria en vocabularios de gran tamaño.

    Attributes:
        raiz (TrieNode): Nodo raíz vacío del Trie.
        _total_palabras (int): Contador de palabras insertadas.

    Complexity:
        Inserción:   O(m) — m = longitud de la palabra.
        Búsqueda:    O(m).
        Sugerencias: O(m + k) — k = número de sugerencias encontradas.

    Example:
        >>> trie = Trie()
        >>> trie.insertar("git commit")
        >>> list(trie.sugerir("git"))
        ['git commit']
    """

    def __init__(self) -> None:
        """Inicializa el Trie con un nodo raíz vacío."""
        self.raiz: TrieNode = TrieNode()
        self._total_palabras: int = 0

    def insertar(self, palabra: str) -> None:
        """Inserta una palabra o comando en el Trie.

        Recorre cada carácter de la palabra creando nodos donde no existan,
        y marca el nodo final como terminal.

        Args:
            palabra (str): Cadena a insertar (ej. 'git commit', 'docker run').

        Raises:
            ValueError: Si la palabra es una cadena vacía.

        Example:
            >>> trie.insertar("docker build")
        """
        if not palabra:
            raise ValueError("La palabra a insertar no puede ser una cadena vacía.")

        nodo: TrieNode = self.raiz
        for caracter in palabra:
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = TrieNode()
            nodo = nodo.hijos[caracter]

        if not nodo.es_fin:
            self._total_palabras += 1
        nodo.es_fin = True
        nodo.palabra_completa = palabra

    def buscar(self, palabra: str) -> bool:
        """Verifica si una palabra completa existe en el Trie.

        Args:
            palabra (str): Palabra a buscar exactamente.

        Returns:
            bool: True si la palabra fue insertada previamente, False si no.

        Example:
            >>> trie.buscar("git commit")
            True
            >>> trie.buscar("git push")
            False
        """
        nodo: Optional[TrieNode] = self._navegar_hasta(palabra)
        return nodo is not None and nodo.es_fin

    def sugerir(self, prefijo: str) -> Generator[str, None, None]:
        """Genera todas las palabras que comienzan con el prefijo dado.

        Implementado como generador (yield) para eficiencia de memoria.
        Evita cargar todas las sugerencias en una lista cuando el vocabulario
        es muy grande.

        Args:
            prefijo (str): Prefijo de búsqueda (ej. 'git', 'docker').

        Yields:
            str: Cada palabra válida que comienza con el prefijo,
                en el orden en que fueron encontradas en el DFS.

        Example:
            >>> for cmd in trie.sugerir("git"):
            ...     print(cmd)
            git commit
            git clone
            git checkout
        """
        nodo: Optional[TrieNode] = self._navegar_hasta(prefijo)
        if nodo is None:
            return
        yield from self._dfs_palabras(nodo)

    def eliminar(self, palabra: str) -> None:
        """Elimina una palabra del Trie si existe.

        Args:
            palabra (str): Palabra a eliminar.

        Raises:
            KeyError: Si la palabra no existe en el Trie.

        Example:
            >>> trie.eliminar("git commit")
        """
        if not self.buscar(palabra):
            raise KeyError(f"La palabra '{palabra}' no existe en el Trie.")
        self._eliminar_recursivo(self.raiz, palabra, 0)
        self._total_palabras -= 1

    def _navegar_hasta(self, prefijo: str) -> Optional[TrieNode]:
        """Navega el Trie hasta el nodo del último carácter del prefijo.

        Args:
            prefijo (str): Cadena de prefijo a navegar.

        Returns:
            Optional[TrieNode]: El nodo al final del prefijo,
                o None si algún carácter no existe en el Trie.
        """
        nodo: TrieNode = self.raiz
        for caracter in prefijo:
            if caracter not in nodo.hijos:
                return None
            nodo = nodo.hijos[caracter]
        return nodo

    def _dfs_palabras(self, nodo: TrieNode) -> Generator[str, None, None]:
        """Recorre en DFS desde un nodo generando todas las palabras terminales.

        Usa yield para producir una palabra a la vez sin acumular resultados,
        lo que permite manejar vocabularios de millones de entradas.

        Args:
            nodo (TrieNode): Nodo raíz del recorrido DFS.

        Yields:
            str: Cada palabra completa encontrada en el subárbol.
        """
        if nodo.es_fin and nodo.palabra_completa is not None:
            yield nodo.palabra_completa
        for hijo in nodo.hijos.values():
            yield from self._dfs_palabras(hijo)

    def _eliminar_recursivo(
        self, nodo: TrieNode, palabra: str, indice: int
    ) -> bool:
        """Elimina una palabra recursivamente, limpiando nodos huérfanos.

        Args:
            nodo (TrieNode): Nodo actual en el recorrido.
            palabra (str): Palabra que se está eliminando.
            indice (int): Índice del carácter actual en la palabra.

        Returns:
            bool: True si el nodo actual puede ser eliminado (sin otros hijos).
        """
        if indice == len(palabra):
            nodo.es_fin = False
            nodo.palabra_completa = None
            return len(nodo.hijos) == 0

        caracter: str = palabra[indice]
        if caracter not in nodo.hijos:
            return False

        debe_eliminar: bool = self._eliminar_recursivo(
            nodo.hijos[caracter], palabra, indice + 1
        )
        if debe_eliminar:
            del nodo.hijos[caracter]
            return len(nodo.hijos) == 0 and not nodo.es_fin

        return False

    @property
    def total_palabras(self) -> int:
        """Retorna el número total de palabras insertadas.

        Returns:
            int: Cantidad de palabras únicas en el Trie.
        """
        return self._total_palabras


# ─── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    trie = Trie()
    comandos = [
        "git commit", "git clone", "git checkout", "git branch", "git push",
        "docker run", "docker build", "docker ps", "docker stop",
        "python manage.py migrate", "python manage.py runserver",
        "pip install", "pip freeze", "pip uninstall",
    ]
    for cmd in comandos:
        trie.insertar(cmd)

    print("=== Autocompletado de Comandos (Trie) ===")
    print(f"Total de comandos indexados: {trie.total_palabras}\n")

    for prefijo in ["git", "docker", "pip", "python", "npm"]:
        sugerencias = list(trie.sugerir(prefijo))
        print(f"Prefijo '{prefijo}' → {len(sugerencias)} resultado(s):")
        for s in sugerencias:
            print(f"    → {s}")

    print(f"\n¿Existe 'git commit'?  {trie.buscar('git commit')}")
    print(f"¿Existe 'git rebase'?  {trie.buscar('git rebase')}")

    trie.eliminar("git push")
    print(f"\nTras eliminar 'git push':")
    print(f"¿Existe 'git push'?    {trie.buscar('git push')}")
    print(f"Sugerencias 'git':     {list(trie.sugerir('git'))}")
    