#include <bits/stdc++.h>
using namespace std;

#define ITER 20000

int N,M,cnt;
char grid[1000][1000];

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin>>N>>M;
    mt19937 rng;
    uniform_int_distribution<int> nrng(0, N-1);
    uniform_int_distribution<int> mrng(0, M-1);
    uniform_int_distribution<int> dr(0, 1);
    for (int i = 0; i < N * M; ++i) {
        cin>>grid[i];
    }
    for (int i = 1; i <= ITER; ++i) {
        int r = 0, c = 0;
        for (int j = 0; j < 100000; j++) {
            while(grid[r][c] == 'T') {
                r = nrng(rng);
                c = mrng(rng);
            }
            if(grid[r][c] == 'P') cnt++;
            if(r == N-1 && c == M-1) {
                break;
            }
            if(r != N-1 && c != M-1) {
                if(dr(rng))r++;
                else c++;
            } else if(r != N-1) r++;
            else c++;
        }
    }
    cout << fixed << setprecision(8);
    cout << (double)cnt/ITER;
}