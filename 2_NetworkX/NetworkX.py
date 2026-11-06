import networkx as nx  # pyright: ignore[reportMissingModuleSource]

# --- Ручное построение графа-«колеса» W_9 ---
G = nx.Graph()
rim = list(range(1, 10))          # вершины обода: 1..9
G.add_node(0)                     # центральный узел
G.add_edges_from((0, v) for v in rim)                       # спицы
G.add_edges_from((rim[i], rim[(i + 1) % 9]) for i in range(9))  # цикл C9

# --- Вычисление центральности в собственных векторах ---
ce = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-12)

print("Центральность в собственных векторах:")
for v in sorted(ce):
    print(f"  узел {v}: {ce[v]:.6f}")

ratio = ce[0] / ce[1]
print(f"\nОтношение x_0 / x_1 = {ratio:.6f}")
print(f"Ожидаемое sqrt(10) - 1 = {10**0.5 - 1:.6f}")


rim_vals = [ce[v] for v in rim]
print("Максимальное отклонение среди вершин обода:",
      max(rim_vals) - min(rim_vals))
