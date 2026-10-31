import heapq

def matrix_to_adjlist(A, zero_means_no_edge=True):
    """
    Преобразует матрицу смежности A в список смежности вида {i: [(j, w), ...]}.

    A[i][j] — вес ребра i-j. Если zero_means_no_edge=True, то A[i][j]==0
    трактуется как отсутствие ребра. Иначе 0 — допустимый вес.
    """
    n = len(A)
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            w = A[i][j]
            if i == j:
                continue
            if zero_means_no_edge and w == 0:
                continue
            adj[i].append((j, w))
    return adj

def dijkstra(adj, start):
    """
    Алгоритм Дейкстры.

    Параметры
    ---------
    adj : dict
        Список смежности: {вершина: [(сосед, вес), ...]}.
        Веса должны быть неотрицательными.
    start : hashable
        Начальная вершина.

    Возвращает
    ----------
    dist : dict {вершина: кратчайшее расстояние от start}
    prev : dict {вершина: предшественник на кратчайшем пути}
    """
    # Инициализация: расстояния бесконечны, предшественники отсутствуют
    dist = {v: float('inf') for v in adj}
    prev = {v: None for v in adj}
    dist[start] = 0

    # Приоритетная очередь: (текущее расстояние, вершина)
    pq = [(0, start)]

    # Множество вершин, для которых расстояние окончательно
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)

        # Устаревшая запись в очереди — пропускаем
        if u in visited:
            continue
        visited.add(u)

        # Релаксация всех исходящих рёбер
        for v, w in adj[u]:
            if w < 0:
                raise ValueError("Алгоритм Дейкстры не работает с отрицательными весами")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev

def reconstruct_path(prev, start, target):
    """Восстанавливает кратчайший путь start -> target по словарю prev."""
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    else:
        return None  # target недостижим
    return path[::-1]


if __name__ == "__main__":

    print("Тест 1: Взвешенный граф из 6 вершин (матрица смежности).")
    # Матрица смежности: 0 — нет ребра (zero_means_no_edge=True)
    A = [
        [ 0,  7,  9,  0, 0, 14],
        [ 7,  0, 10, 15, 0,  0],
        [ 9, 10,  0, 11, 0,  2],
        [ 0, 15, 11,  0, 6,  0],
        [ 0,  0,  0,  6, 0,  9],
        [14,  0,  2,  0, 9,  0],
    ]

    adj = matrix_to_adjlist(A, zero_means_no_edge=True)
    dist, prev = dijkstra(adj, start=0)

    print("Кратчайшие расстояния от вершины 0:")
    for v in sorted(dist):
        print(f"  d(0, {v}) = {dist[v]:>4}  путь: {reconstruct_path(prev, 0, v)}")


    print("Тест 2. Список смежности (неориентированный граф).")
    adj2 = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)],
    }
    dist2, prev2 = dijkstra(adj2, start='A')
    print(dist2)

    print("Тест 3. Несвязный граф (проверка недостижимых вершин).")
    adj3 = {
        0: [(1, 2)],
        1: [(0, 2)],
        2: [(3, 1)],
        3: [(2, 1)],
    }
    dist3, prev3 = dijkstra(adj3, start=0)
    print(dist3)
