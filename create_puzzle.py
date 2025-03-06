import random

def debug_pretty_print(graph):
    for line in graph:
        print(*line)

def debug_checkup_bruteforce(graph):
    pass

def create_random(n: int, m: int = None):
    if m is None:
        m = n

    graph = [[0] * n for i in range(n)]
    pool = [i for i in range(1, n*n + 1)]

    for idx in range(1, m + 1):
        for j in range(2):
            pos = random.choice(pool)
            pool.remove(pos)

            graph[pos//n - 1][pos%n - 1] = idx

    debug_pretty_print(graph)
    return graph

if __name__ == "__main__":
    create_random(5, 5)

"""
test true
3 0 0 3 0
4 0 0 0 0
2 1 0 1 0
0 0 0 0 0
2 0 0 4 0

2 2 0 0 0
3 0 4 4 1
0 3 0 0 0
0 0 0 1 0
0 0 0 0 0
"""