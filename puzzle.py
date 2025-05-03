class Puzzle:
    """
    Класс <Puzzle> реализует внутреннее представление головоломки,
    а также методы корректного взаимодействия с ней.
    """

    def __init__(self, size, count_points, graph):
        self._size = size
        self._graph = graph
        self._count_points = count_points

        # список всех решений головоломки
        self._results = []
        # список словарей путей для каждой пары чисел
        self._paths = []
        # статус головоломки (решена / не решена)
        self._status = False

    # флаг пуста ли головоломка
    def is_empty(self) -> bool:
        return self._size == 0 or self._graph == [] or self._count_points == 0

    # флаг решена ли головоломка
    def is_solved(self) -> bool:
        return self._status

    def get_result(self) -> tuple[list[list], list]:
        """
        Генераторная функция, возвращающая пару - готовое решение
        и пути в этом решении

        :return: возвращает конструкцию типов: tuple[list[list], list]
        """
        for idx, result in enumerate(self._results):
            yield result, self._paths[idx]

    # возвращает граф
    def get_graph(self) -> list[list]:
        return self._graph

    # возвращает размер головоломки
    def get_size(self) -> int:
        return self._size

    # возвращает количество различных пар чисел в головоломке
    def get_count_points(self) -> int:
        return self._count_points

    # поставить флаг готовности
    def set_is_solved(self) -> None:
        self._status = True

    # установить поле self._paths
    def set_paths(self, paths: list[dict]) -> None:
        self._paths = paths

    # установить поле self._results
    def set_result(self, results: list[list]) -> None:
        self._results = results
