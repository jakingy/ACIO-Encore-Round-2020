#include <bits/stdc++.h>
using namespace std;

#define MAXNM (5000 * 5000)

int N,M;
double dp[MAXNM][2], psm, tsm, tavg;
char grid[MAXNM];

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin>>N>>M;
    for (int i = 0; i < N * M; ++i) {
        cin>>grid[i];
    }
    for (int n = N; n-->0;) {
        for (int m = M; m-->0;) {
            if (grid[n*M+m] == 'T') dp[n*M+m][1] = 1;
            else {
                int op = 0;
                if (m < M-1) {
                    op++;
                    dp[n*M+m][0] += dp[n*M+m+1][0];
                    dp[n*M+m][1] += dp[n*M+m+1][1];
                }
                if (n < N-1) {
                    op++;
                    dp[n*M+m][0] += dp[n*M+m+M][0];
                    dp[n*M+m][1] += dp[n*M+m+M][1];
                }
                if (op) {
                    dp[n*M+m][0] /= op;
                    dp[n*M+m][1] /= op;
                }
                dp[n*M+m][0] += (grid[n*M+m] == 'P');               
            }
            // cout << n << " " << m << " " << dp[n*M+m][0] << " " << dp[n*M+m][1] << "\n";
            psm += dp[n*M+m][0];
            tsm += dp[n*M+m][1];
        }
    }
    cout << fixed << setprecision(8);
    tavg = psm/(N*M-tsm);
    cout << dp[0][0] + tavg * dp[0][1] << "\n";
}