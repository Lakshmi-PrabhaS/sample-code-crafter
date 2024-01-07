from typing import List, Tuple
from queue import Queue

class Graph:
    def __init__(self):
        self.parent = []
        self.rows = 0
        self.cols = 0

    def find(self, x):
        return x if self.parent[x] == x else self.find(self.parent[x])

    def dfs(self, A, i, j):
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return

        if A[i][j] != 1:
            return

        A[i][j] = -1
        self.dfs(A, i + 1, j)
        self.dfs(A, i - 1, j)
        self.dfs(A, i, j + 1)
        self.dfs(A, i, j - 1)

    def find_redundant_connection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)

        self.parent = [i for i in range(n + 1)]

        res = [0, 0]
        for edge in edges:
            x = self.find(edge[0])
            y = self.find(edge[1])
            if x != y:
                self.parent[y] = x
            else:
                res = edge

        return res

    def num_enclaves(self, A: List[List[int]]) -> int:
        if not A:
            return 0

        self.rows = len(A)
        self.cols = len(A[0])

        for i in range(self.rows):
            for j in range(self.cols):
                if i == 0 or j == 0 or i == self.rows - 1 or j == self.cols - 1:
                    self.dfs(A, i, j)

        ans = sum(row.count(1) for row in A)
        return ans

    def update_matrix(self, matrix: List[List[int]]) -> List[List[int]]:
        if not matrix:
            return matrix

        rows = len(matrix)
        cols = len(matrix[0])
        queue = Queue()

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    queue.put((i - 1, j))
                    queue.put((i + 1, j))
                    queue.put((i, j - 1))
                    queue.put((i, j + 1))

        visited = [[False] * cols for _ in range(rows)]
        steps = 0

        while not queue.empty():
            steps += 1
            size = queue.qsize()
            for _ in range(size):
                front = queue.get()
                l, r = front[0], front[1]
                if 0 <= l < rows and 0 <= r < cols and not visited[l][r] and matrix[l][r] == 1:
                    visited[l][r] = True
                    matrix[l][r] = steps
                    queue.put((l - 1, r))
                    queue.put((l + 1, r))
                    queue.put((l, r - 1))
                    queue.put((l, r + 1))

        return matrix
