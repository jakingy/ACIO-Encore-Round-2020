#include <bits/stdc++.h>
using namespace std;

#define MAXS 1000001
int S, R, M, C, p[MAXS], scc[2*MAXS], g[2*MAXS], cnt, scnt, tcnt, seen[2*MAXS], invalid;
vector<int> adj[2*MAXS], impl[2*MAXS], inv[2*MAXS], used;
stack<int> order;

int ne(int x) {
    return ((long long)x * C) % M;
}

int notX(int x) {
    return x * 2 + 1;
}

int isX(int x) {
    return x * 2;
}

void dfs1(int u) {
    seen[u] = 1;
    for (int v: impl[u]) if (!seen[v]) dfs1(v);
    order.push(u);
}

void dfs2(int u) {
    scc[u] = scnt;
    for (int v: inv[u]) if (!scc[v]) dfs2(v);
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    ifstream input_file("stalls.in");
    input_file >> S >> R >> M >> C;
    for (int i = 1; i <= S; ++i) {
        input_file >> p[i];
        p[i] %= M;
    }
    for (int i = 0,a,b; i < R; ++i) {
        input_file >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
        if (p[a] == p[b]) {
            impl[isX(a)].push_back(notX(b)); 
            impl[notX(a)].push_back(isX(b)); 
            impl[isX(b)].push_back(notX(a)); 
            impl[notX(b)].push_back(isX(a));  
        }
        if (ne(p[a]) == p[b]) {
            if (ne(p[b]) == p[b]){
                impl[notX(a)].push_back(notX(b));
                impl[isX(a)].push_back(notX(b));
            } 
            impl[isX(a)].push_back(isX(b));
            impl[notX(b)].push_back(notX(a));
        }
        if (ne(p[b]) == p[a]) {
            if (ne(p[a]) == p[a]){
                impl[notX(b)].push_back(notX(a));
                impl[isX(b)].push_back(notX(a));
            } 
            impl[isX(b)].push_back(isX(a));
            impl[notX(a)].push_back(notX(b));
        }
        if (ne(p[b]) == ne(p[a])) { // bug without this
            impl[isX(a)].push_back(notX(b));
            impl[isX(b)].push_back(notX(a));
        }
    }
    
    for (int i = 2; i < S*2+2; ++i)
        for (int v: impl[i])
            inv[v].push_back(i);

    for (int i = 2; i < S*2+2; ++i) {
        if (!seen[i]) dfs1(i);
    }
    while (order.size()) {
        scnt++;
        int x = order.top();
        order.pop();
        if (!scc[x]) dfs2(x);
    }
    for (int i = 1; i <= S; ++i) {
        if (scc[isX(i)] == scc[notX(i)]) {
            invalid = 1;
            break;
        }
    }

    ifstream contestant_output("stalls.out");
    int n;
    bool ac = 1;
    contestant_output >> n;
    if (invalid) {
        if (n != -1) {
            cout << "this case was meant to be impossible\n";
            ac = 0; 
        }
    }
    else {
        vector<int> stalls;
        int stall;
        while (contestant_output >> stall) stalls.push_back(stall);
        if (n != stalls.size()) {
            cout << "powers used more than indicated\n";
            ac = 0;
        }
        if(set<int>(stalls.begin(), stalls.end()).size() != stalls.size()) {
            cout << "used power twice\n";
            ac = 0;
        }
        for (int stall: stalls) {
            if (stall < 1 || stall > S) {
                cout << "out of bounds\n";
                ac = 0;
                break;
            }
            p[stall] = ne(p[stall]);
        }
        for (int i = 1; i <= S && ac; ++i) {
            for (int v: adj[i]) {
                if (p[i] == p[v]) {
                    ac = 0;
                    cout << "not special\n";
                    break;
                }
            }
        }
    }

    if (ac)
        cout << 100;
    else
        cout << 0;
    cout << endl;
}