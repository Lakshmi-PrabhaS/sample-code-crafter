class Graph {
 	vector<int>parent;
 	int find(int x) {
 		return parent[x] == x ? x : find(parent[x]);
 	}

    int rows, cols;
 	void dfs(vector<vector<int>>& A, int i, int j) {
 		if (i < 0 || j < 0 || i >= rows || j >= cols)
 			return;

 		if (A[i][j] != 1) 
 			return;

 		A[i][j] = -1;
 		dfs(A, i+1, j);
 		dfs(A, i-1, j);
 		dfs(A, i, j+1);
 		dfs(A, i, j-1);
 	}
 public:
 	vector<int> findRedundantConnection(vector<vector<int>>& edges) {
 		int n = edges.size();

 		parent.resize(n+1, 0);
 		for (int i = 0; i <= n; i++)
 			parent[i] = i;

 		vector<int>res(2, 0);
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
  
    int numEnclaves(vector<vector<int>>& A) {
 		if (A.empty()) return 0;

 		rows = A.size();
 		cols = A[0].size();
 		for (int i = 0; i < rows; i++) {
 			for (int j = 0; j < cols; j++) {
 				if (i == 0 || j == 0 || i == rows-1 || j == cols-1)
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

    vector<vector<int>> updateMatrix(vector<vector<int>>& matrix) {

		if (matrix.empty()) return matrix;
		int rows = matrix.size();
		int cols = matrix[0].size();
		queue<pair<int, int>>pq;
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				if (matrix[i][j] == 0) {
					pq.push({i-1, j}), pq.push({i+1, j}), pq.push({i, j-1}), pq.push({i, j+1}); 
				}
			}
		}

		vector<vector<bool>>visited(rows, vector<bool>(cols, false));
		int steps = 0;
		while (!pq.empty()) {
			steps++;
			int size = pq.size();
			for (int i = 0; i < size; i++) {
				auto front = pq.front();
				int l = front.first;
				int r = front.second;
				pq.pop();
				if (l >= 0 && r >= 0 && l < rows && r < cols && !visited[l][r] && matrix[l][r] == 1) {
					visited[l][r] = true;
					matrix[l][r] = steps;
					pq.push({l-1, r}), pq.push({l+1, r}), pq.push({l, r-1}), pq.push({l, r+1});
				}
			}
		}

		return matrix;
	}
 };
