#include <bits/stdc++.h>
using namespace std;

//requires alotta stack, breaks on windows unless use 
// g++ code.cpp -o test.exe -Wl,--stack,STACK_SIZE_BYTES

#define MAXS 1000001
int S, R, M, C, p[MAXS], scc[2*MAXS], g[2*MAXS], cnt, scnt, tcnt, seen[2*MAXS], invalid;
vector<int> impl[2*MAXS], inv[2*MAXS], used;
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
    cin >> S >> R >> M >> C;
    for (int i = 1; i <= S; ++i) {
        cin >> p[i];
        p[i] %= M;
    }
    for (int i = 0,a,b; i < R; ++i) {
        cin >> a >> b;
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
        cout << scc[isX(i)] << " " << scc[notX(i)] <<"\n";
        if (scc[isX(i)] == scc[notX(i)]) {
            invalid = 1;
            break;
        }
        if (scc[notX(i)] < scc[isX(i)]) {
            used.push_back(i);
        }
    }

    if (invalid) {
        cout << "-1";    
    } else {
        cout << used.size() << "\n";
        for (int i: used) cout << i << " ";   
    }
    cout << "\n";
}