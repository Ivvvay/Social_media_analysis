import networkx as nx  # pyright: ignore[reportMissingModuleSource]
import numpy as np  # pyright: ignore[reportMissingImports]

n = 150
p = 0.05

# --- Генерация графа в модели Эрдёша–Реньи G(n, p) ---
G = nx.erdos_renyi_graph(n, p, seed=42)

# --- Эмпирические характеристики ---
m_hat = G.number_of_edges()                       # число рёбер
deg = np.array([d for _, d in G.degree()])         # степени вершин
c_hat = deg.mean()                                 # средняя степень
c_theor = (n - 1) * p                              # формула из лекции
print("\n--- Генерация графа в модели Эрдёша–Реньи G(n, p) ---")
print(f"\nЧисло вершин n = {G.number_of_nodes()}")
print(f"Число рёбер m = {m_hat}")
print(f"Средняя степень (программа) c = {c_hat:.4f}")
print(f"Средняя степень (формула)   c = {c_theor:.4f}")
print(f"Отклонение |c_hat - c_theor| = {abs(c_hat - c_theor):.4f}")
print(f"Среднее число рёбер по формуле: {n*(n-1)/2*p:.2f}")

# --- Дополнительно: коэффициент кластеризации и компоненты ---
print(f"\nКоэффициент кластеризации: {nx.average_clustering(G):.4f} (теория: p = {p})")
comps = sorted(nx.connected_components(G), key=len, reverse=True)
print(f"Число компонент связности: {len(comps)}")
print(f"Размер наибольшего компонента: {len(comps[0])} ({len(comps[0])/n:.4f} от n)")



# --- Оценка разброса по ансамблю ---
K = 100
c_samples = np.empty(K)
m_samples = np.empty(K)

for k in range(K):
    Gk = nx.erdos_renyi_graph(n, p, seed=1000 + k)
    degk = np.array([d for _, d in Gk.degree()])
    c_samples[k] = degk.mean()
    m_samples[k] = Gk.number_of_edges()
print("\n--- Оценка разброса по ансамблю ---")
print(f"\nСреднее по {K} реализациям: <c> = {c_samples.mean():.4f}")
print(f"Стандартное отклонение c: {c_samples.std(ddof=1):.4f}")
print(f"Среднее число рёбер: <m> = {m_samples.mean():.2f}")
print(f"Теория: c = {c_theor:.4f}, m = {n*(n-1)/2*p:.2f}")

# Теоретическое стандартное отклонение средней степени:
# Var(k_i) = (n-1)p(1-p); усреднение по n вершинам даёт Var(c_hat) = (n-1)p(1-p)/n
sigma_theor = np.sqrt((n - 1) * p * (1 - p) / n)
print(f"Теоретическое СКО средней степени: {sigma_theor:.4f}")



# --- Проверка распределения степеней (Пуассон) ---
from collections import Counter  # noqa: E402

deg = np.array([d for _, d in G.degree()])
counts = Counter(deg)
ks = np.arange(deg.min(), deg.max() + 1)

import math  # noqa: E402
poisson_pmf = np.array([math.exp(-c_theor) * c_theor**k / math.factorial(k) for k in ks])
empirical_pmf = np.array([counts.get(k, 0) / n for k in ks])

print("\n--- Проверка распределения степеней (Пуассон) ---")
print(" k | наблюд. | Пуассон")
for k, emp, th in zip(ks, empirical_pmf, poisson_pmf):
    print(f"{k:2d} | {emp:.4f}  | {th:.4f}")
