#include <bits/stdc++.h>
using namespace std;

int S,R,M,C,used[1<<20];

int ne(int x) {
    return ((long long)x * C) % M;
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> S >> R >> M >> C;
    map<int, int> seen;
    for (int i = 0,p; i < S; ++i) {
        cin >> p;
        p %= M;
        if (seen.count(p)) {
            int x = i;
            used[i] = 1;
            p = ne(p);
            while (seen.count(p)) {
                if (used[seen[p]]) {
                    cout << -1;
                    exit(0);
                }
                swap(x, seen[p]);
                used[x] = 1;
                p = ne(p);
            }
            seen[p] = x;
        }
        else seen[p] = i;
    }
    vector<int> power;
    for (int i = 0; i < S; ++i) {
        if (used[i]) power.push_back(i);
    }
    cout << power.size() << "\n";
    for (int s: power) cout << s + 1 << " ";
}