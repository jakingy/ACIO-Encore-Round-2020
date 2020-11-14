#include <bits/stdc++.h>
using namespace std;

#define MAXN 1000

int N, M, done[MAXN][MAXN];
double cache[MAXN][MAXN];
char grid[MAXN][MAXN];

double E(int r, int c) {
    if (!done[r][c]) {
        done[r][c] = 1;
        if (r < N - 1 && c < M - 1) cache[r][c] = .5 * E(r + 1, c) + .5 * E(r, c + 1);
        else if(r < N - 1) cache[r][c] = E(r + 1, c);
        else if(c < M - 1) cache[r][c] = E(r, c + 1);
        cache[r][c] += grid[r][c] == 'P';
    }
    return cache[r][c];
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin>>N>>M;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < M; ++j) {
            cin>>grid[i][j];
        }
    }
    cout << fixed << setprecision(8);
    cout << E(0,0) << "\n";
}