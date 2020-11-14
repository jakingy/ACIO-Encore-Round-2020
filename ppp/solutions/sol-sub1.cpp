#include <bits/stdc++.h>
using namespace std;

#define MAXN (1<<17)
#define MAXQ MAXN

int H, Q, X[MAXQ]; 
long double a[MAXN], b[MAXN], R, rev[MAXN];

long double dfs(int x, int d = 0) {
    if (d < H && a[x] <= R && R <= b[x]) {
        rev[x] = dfs(x*2, d + 1) + dfs(x*2+1, d + 1);
        return 10 + rev[x] * R;
    }
    return 0;
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> H;
    b[1] = 1;
    for(int i = 2; i < (1<<H); ++i) {
        cin>>a[i]>>b[i];
    }
    cin>>Q;
    for(int i = 0; i < Q; ++i){
        cin>>X[i]>>R;
    }
    dfs(1);
    cout << fixed << setprecision(6);
    for(int i = 0; i < Q; ++i){
        cout << rev[X[i]] << "\n";
    }
}