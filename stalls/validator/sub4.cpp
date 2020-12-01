#include "common.h"

#define top back
#define pop pop_back
#define push push_back

int cnt, seen[MAX_S + 1];
void dfs(Checker &c, int u) {
	vector<int> s;
	s.push(u);
	while (s.size()) {
		int u = s.top();
		s.pop();
		if (!seen[u]) {
			seen[u] = 1;
			cnt++;
			for (int v: c.adj[u])
				s.push(v);
		}
	}
}

int main() {
	Checker c{}; c.validate();
	ensuref(c.R == c.S-1, "Graph is not a tree.");
	dfs(c,1);
	ensuref(cnt == c.S, "Graph is not a tree.");
	return 0;
}
