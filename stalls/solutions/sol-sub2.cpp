#include <bits/stdc++.h>
using namespace std;

int S,R,M,C,p[18],pt[18];
vector<int> adj[18];

int ne(int x) {
    return ((long long)x * C) % M;
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> S >> R >> M >> C;
    for (int i = 0; i < S; ++i) {
        cin >> p[i];
        p[i] %= M;
    }
    for (int i = 0,a,b; i < R; ++i) {
        cin >> a >> b;
        adj[a-1].push_back(b-1);
    }
    for (int i = 0; i < (1<<S); ++i) {
        for (int j = 0; j < S; ++j) {
            pt[j] = p[j];
            if((i>>j)&1) pt[j] = ne(pt[j]);
        }
        bool valid = 1;
        for (int i = 0; i < S && valid; ++i) {
            for (int v: adj[i]) {
                if (pt[i] == pt[v]) {
                    valid = 0;
                    break;
                }
            }
        }
        if (valid) {
            vector<int> power;
            for (int j = 0; j < S; ++j) {
                if((i>>j)&1) power.push_back(j);
            }
            cout << power.size() << "\n";
            for (int s: power) cout << s + 1 << " ";
            return 0;
        }
    }
    cout << -1;
}