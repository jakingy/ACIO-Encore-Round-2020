#include <bits/stdc++.h>
using namespace std;

#define MAXN (1<<17)
#define MAXQ MAXN

int H, Q, X, cnt[MAXN][17], join[MAXN]; 
double a[MAXN], b[MAXN], R, ans[MAXQ];

struct ev {
    double r;
    int tp, x;
};

bool operator < (ev a, ev b) {
    if (a.r != b.r) {
        return a.r < b.r;
    }
    if (a.tp != b.tp) {
        return a.tp < b.tp;
    }
    return a.x < b.x;
}

struct qry {
    double r;
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
    join[e.x] = 1-e.tp;
    int x = e.x;
    //cout << "Resolving " << e.x << " " << e.r << " " << e.tp << "\n";
    do {
        x = par(x);
        //cout << "cnt " << x << ": ";
        for (int i = 0; i < H; ++i){
            if (e.tp) {
                cnt[x][i] -= cnt[e.x][i];
            }else {
                cnt[x][i] += cnt[e.x][i];
            }
            //cout << cnt[x][i] << " ";
        }
        //cout << endl;
        
    } while(join[x]);
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cin >> H;
    vector<ev> es;
    for(int i = 1; i < (1<<H)-1; ++i) {
        cin>>a[i]>>b[i];
        es.push_back({a[i], 0, i});
        es.push_back({b[i], 1, i});
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
    for(int i = 0; i < Q; ++i){
        while (eptr < es.size() && ((es[eptr].r < qs[i].r) || (es[eptr].r == qs[i].r && es[eptr].tp == 0))) {
            resolve_event(es[eptr]);
            eptr++;
        }

        //cout << "Querying " << qs[i].x << " " << qs[i].r << " " << qs[i].id << "\n";

        /*cout << "cnt " << qs[i].x << ": ";
        for (int i = 0; i < H; ++i){
            cout << cnt[qs[i].x][i] << " ";
        }
        cout << endl;*/

        double p = 1;
        for (int d = depth(qs[i].x)+1; d < H; ++d) {
            ans[qs[i].id] += p * cnt[qs[i].x][d];
            p *= qs[i].r;
        }

        //check if broken
        for(int j = qs[i].x; j > 0; j = par(j)) {
            if (!join[j]) ans[qs[i].id] = 0;
        }

        while (eptr < es.size() && es[eptr].r == qs[i].r) {
            resolve_event(es[eptr]);
            eptr++;
        }
    }

    for(int i = 0; i < Q; ++i) {
        cout << ans[i]*10 << "\n";
    }
}