#include <bits/stdc++.h>
using namespace std;

#define MAXN 1000

int N,M;
long double dpP[MAXN * MAXN], dpT[MAXN * MAXN], smP, smT, T;
char grid[MAXN * MAXN];

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin>>N>>M;
    for (int i = 0; i < N * M; ++i) cin>>grid[i];
    for (int n = N; n-->0;) {
        for (int m = M; m-->0;) {
            if (grid[n*M+m] == 'T') dpT[n*M+m] = 1;
            else {
                if (n < N-1 && m < M-1) {
                    dpP[n*M+m] += (dpP[n*M+m+1] + dpP[n*M+m+M]) / 2;
                    dpT[n*M+m] += (dpT[n*M+m+1] + dpT[n*M+m+M]) / 2;
                }
                else if (n < N-1) {
                    dpP[n*M+m] = dpP[n*M+m+M];
                    dpT[n*M+m] = dpT[n*M+m+M];
                }
                else if (m < M-1) {
                    dpP[n*M+m] = dpP[n*M+m+1];
                    dpT[n*M+m] = dpT[n*M+m+1];
                }
                dpP[n*M+m] += (grid[n*M+m] == 'P');               
            }
            smP += dpP[n*M+m];
            smT += dpT[n*M+m];
        }
    }
    cout << fixed << setprecision(8);
    T = smP/(N*M-smT);
    cout << dpP[0] + T * dpT[0] << "\n";
}