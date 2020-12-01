#include <bits/stdc++.h>
using namespace std;

#define MAXS 1000001
int S,R,M,C,p[MAXS];
vector<int> adj[MAXS], power;

int ne(int x) {
    return ((long long)x * C) % M;
}

void invalid() {
    cout << -1;
    exit(0);
}

void dfs(int u, int par) {
    if (p[u] == p[par]) {
        p[u] = ne(p[u]);
        power.push_back(u);
        if (p[u] == p[par]) invalid();
    }
    for (int v: adj[u]) if (v != par) {
        dfs(v, u);
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
    p[0] = -1;
    dfs(1,0);
    cout << power.size() << "\n";
    for (int s: power) cout << s << " ";
}