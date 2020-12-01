#include <bits/stdc++.h>
using namespace std;

#define MAXS 1000001
int S,R,M,C,p[MAXS],cache[MAXS][2],done[MAXS][2];
vector<int> adj[MAXS], power;

int ne(int x) {
    return ((long long)x * C) % M;
}

int dp(int u, int par, bool pow) { //0 impossible, 1 did not flip, 2 flipped
    if (!done[u][pow]) {
        done[u][pow] = 1;
        int pp = p[par];
        if (pow) pp = ne(pp);
        if (p[u] != pp) {
            bool valid = 1;
            for (int v: adj[u]) if (v != par) {
                if (!dp(v, u, 0)) {
                    valid = 0; 
                    break;
                }
            }
            if (valid) cache[u][pow] = 1;
        }
        if (!cache[u][pow] && ne(p[u]) != pp) {
            bool valid = 1;
            for (int v: adj[u]) if (v != par) {
                if (!dp(v, u, 1)) {
                    valid = 0; 
                    break;
                }
            }
            if (valid) cache[u][pow] = 2;
        }
    }
    return cache[u][pow];
}

void dfs(int u, int par, bool pow) { //0 impossible, 1 did not flip, 2 flipped
    bool upow = cache[u][pow] == 2;
    if (upow) power.push_back(u);
    for (int v: adj[u]) if (v != par) {
        dfs(v, u, upow);
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
    dp(1,0,0);
    if (!cache[1][0]) {
        cout << -1;
    } else {
        dfs(1,0,0);
        cout << power.size() << "\n";
        for (int s: power) cout << s << " ";
    }
}