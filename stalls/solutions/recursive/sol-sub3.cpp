#include <bits/stdc++.h>
using namespace std;

#define MAXS 1000001
int S,R,M,C,p[MAXS],seen[MAXS];
vector<int> adj[MAXS], power;

void invalid() {
    cout << -1;
    exit(0);
}

void dfs(int u, int c) {
    if (seen[u]) {
        if (p[u] != c) invalid();
    } else {
        seen[u] = 1;
        if (p[u] != c) {
            p[u] = c;
            power.push_back(u);
        }
        for (int v: adj[u]) dfs(v, 3-c);
    }
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> S >> R >> M >> C;
    for (int i = 1; i <= S; ++i) {
        cin >> p[i];
        p[i] %= M;
    }
    for (int i = 0,a,b; i < R; ++i) {
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    for (int i = 1; i <= S; ++i) {
        if (!seen[i]) dfs(i,p[i]);
    }
    cout << power.size() << "\n";
    for (int s: power) cout << s << " ";
}