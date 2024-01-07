import java.util.*;

public class Graph {
    private int[] parent;
    private int rows, cols;

    private int find(int x) {
        return parent[x] == x ? x : find(parent[x]);
    }

    private void dfs(int[][] A, int i, int j) {
        if (i < 0 || j < 0 || i >= rows || j >= cols)
            return;

        if (A[i][j] != 1)
            return;

        A[i][j] = -1;
        dfs(A, i + 1, j);
        dfs(A, i - 1, j);
        dfs(A, i, j + 1);
        dfs(A, i, j - 1);
    }

    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;

        parent = new int[n + 1];
        for (int i = 0; i <= n; i++)
            parent[i] = i;

        int[] res = new int[2];
        for (int i = 0; i < n; i++) {
            int x = find(edges[i][0]);
            int y = find(edges[i][1]);
            if (x != y)
                parent[y] = x;
            else {
                res[0] = edges[i][0];
                res[1] = edges[i][1];
            }
        }

        return res;
    }

    public int numEnclaves(int[][] A) {
        if (A.length == 0)
            return 0;

        rows = A.length;
        cols = A[0].length;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (i == 0 || j == 0 || i == rows - 1 || j == cols - 1)
                    dfs(A, i, j);
            }
        }

        int ans = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (A[i][j] == 1)
                    ans++;
            }
        }

        return ans;
    }

    public int[][] updateMatrix(int[][] matrix) {
        if (matrix.length == 0)
            return matrix;

        int rows = matrix.length;
        int cols = matrix[0].length;
        Queue<int[]> queue = new LinkedList<>();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == 0) {
                    queue.offer(new int[]{i - 1, j});
                    queue.offer(new int[]{i + 1, j});
                    queue.offer(new int[]{i, j - 1});
                    queue.offer(new int[]{i, j + 1});
                }
            }
        }

        boolean[][] visited = new boolean[rows][cols];
        int steps = 0;
        while (!queue.isEmpty()) {
            steps++;
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                int[] front = queue.poll();
                int l = front[0];
                int r = front[1];
                if (l >= 0 && r >= 0 && l < rows && r < cols && !visited[l][r] && matrix[l][r] == 1) {
                    visited[l][r] = true;
                    matrix[l][r] = steps;
                    queue.offer(new int[]{l - 1, r});
                    queue.offer(new int[]{l + 1, r});
                    queue.offer(new int[]{l, r - 1});
                    queue.offer(new int[]{l, r + 1});
                }
            }
        }

        return matrix;
    }
}
