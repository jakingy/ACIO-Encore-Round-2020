#include <bits/stdc++.h>
using namespace std;

#define MAXN (1<<17)
#define MAXQ MAXN

int H, Q, X; 
long double a[MAXN], b[MAXN], R;

int par(int x){return (x-1)/2;}

int depth(int x){
    return 31-__builtin_clz(x+1);
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> H;
    for(int i = 1; i < (1<<H)-1; ++i) {
        cin>>a[i]>>b[i];
    }
    cin>>Q;
    //cout << fixed << setprecision(6);
    for(int i = 0; i < Q; ++i){
        cin>>X>>R;
        X--;
        int ans = 0;
        if (a[X*2+2] <= R && R <= b[X*2+2]) {
            ans += 10;
        }
        if (a[X*2+1] <= R && R <= b[X*2+1]) {
            ans += 10;
        }
        for(int j = X; j > 0; j = par(j)) {
            if (R < a[j] || b[j] < R) ans = 0;
        }
        cout << ans << "\n";
    }
}