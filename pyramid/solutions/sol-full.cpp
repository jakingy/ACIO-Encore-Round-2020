#include <bits/stdc++.h>
using namespace std;

#define MAXH 17
#define MAXN (1<<MAXH)
#define MAXQ MAXN

int H, Q, X, cnt[MAXN][MAXH]; 
long double a[MAXN], b[MAXN], R, ans[MAXQ];

struct ev {
    long double r;
    int tp, x;
};

//make sure breaking case for if tp is not sorted
bool operator < (ev a, ev b) {
    if (a.r != b.r) {
        return a.r < b.r;
    }
    if (a.tp != b.tp) {
        return a.tp > b.tp;
    }
    return a.x < b.x;
}

struct qry {
    long double r;
    int x, id;
};

bool operator < (qry a, qry b) {
    if (a.r != b.r) {
        return a.r < b.r;
    }
    return a.id < b.id;
}

int par(int x){return (x-1)/2;}

int depth(int x){
    return 31-__builtin_clz(x+1);
}

void resolve_event(ev e) {
    int x = e.x, d = depth(e.x);
    while(x) {
        x = par(x);
        cnt[x][d] += e.tp; 
    }
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> H;
    vector<ev> es;
    b[0] = 1;
    for(int i = 1; i < (1<<H)-1; ++i) {
        cin>>a[i]>>b[i];
        a[i] = max(a[i], a[par(i)]);
        b[i] = min(b[i], b[par(i)]);
        if (a[i] <= b[i]) {
            es.push_back({a[i], 1, i});
            es.push_back({b[i], -1, i});
        }
        cnt[i][depth(i)]++;
    }
    sort(es.begin(), es.end());
    cin>>Q;
    vector<qry> qs;
    for(int i = 0; i < Q; ++i){
        cin>>X>>R;
        qs.push_back({R,X-1,i});
    }
    sort(qs.begin(), qs.end());
    int eptr = 0;
    for(int i = 0; i < Q; ++i) {
        while (eptr < es.size() && ((es[eptr].r < qs[i].r) || (es[eptr].r == qs[i].r && es[eptr].tp == 1))) {
            resolve_event(es[eptr]);
            eptr++;
        }

        long double p = 1;
        for (int d = depth(qs[i].x)+1; d < H; ++d) {
            ans[qs[i].id] += p * cnt[qs[i].x][d];
            p *= qs[i].r;
        }
    }

    cout << fixed << setprecision(8);

    for(int i = 0; i < Q; ++i) {
        cout << ans[i]*10 << "\n";
    }
}