#include <bits/stdc++.h>
using namespace std;

//requires alotta stack, breaks on windows unless use 
// g++ code.cpp -o test.exe -Wl,--stack,STACK_SIZE_BYTES

#define MAXS 1000001
int S, R, M, C, p[MAXS];
vector<int> adj[MAXS];
queue<int> q;
using pii = pair<int,int>;

void invalid() {
    cout << -1;
    exit(0);
}

int ne(int x) {
    return ((long long)x * C) % M;
}

void solve() {
    priority_queue<pii> q;
    vector<int> power;
    vector<int> used(S+1), inq(S+1), pt(p, p+S+1);
    
    for (int a = 1; a <= S; ++a) {
        for (int b: adj[a]) {
            if (pt[a] == pt[b]) {
                if (!inq[a]) {
                    q.push({rand(),a});
                    inq[a] = 1;
                }
                if (!inq[b]) {
                    q.push({rand(),b});
                    inq[b] = 1;
                }
            }
        }
    }

    while(q.size()) {
        pii u = q.top();
        q.pop();
        inq[u.second] = 0;
        for (int v: adj[u.second]) {
            if (pt[u.second] == pt[v]){
                pt[u.second] = ne(pt[u.second]);
                used[u.second] = 1;
                power.push_back(u.second);
                break;
            }
        }
        for (int v: adj[u.second]) {
            if (pt[u.second] == pt[v] && !inq[v]){
                if(!used[v]){
                    inq[v] = 1;
                    q.push({rand(),v});
                } else return;
            }
        }
    }

    cout << power.size() << "\n";
    for (int s: power) cout << s << " ";
    exit(0);
}

int main() {
    srand(time(NULL));
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

    for(int i = 0; i < 10; ++i) solve();
    invalid();
}