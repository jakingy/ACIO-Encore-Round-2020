#ifndef COMMON_H
#define COMMON_H
#include "testlib.h"
#include "bounds.h"
using namespace std;

struct Checker {
	int S, R, M, C;
	vector<vector<int>> adj;
	vector<int> p;
	void validate() {
		registerValidation();
		S = inf.readInt(MIN_S, MAX_S, "S");
		inf.readSpace();
		R = inf.readInt(MIN_R, MAX_R, "R");
		inf.readSpace();
		M = inf.readInt(MIN_M, MAX_M, "M");
		inf.readSpace();
		C = inf.readInt(MIN_C, MAX_C, "C");
		inf.readEoln();
		p.resize(S+1);
		for (int i = 1; i <= S; i++) {
			p[i] = inf.readDouble(MIN_P, MAX_P, "p_i");
			inf.readEoln();
		}
		set<pair<int,int>> seen;
		adj.resize(S+1);
		for (int i = 0,a,b; i < R; i++) {
			a = inf.readDouble(1, S, "a_i");
			inf.readSpace();
			b = inf.readDouble(1, S, "b_i");
			ensuref(a != b, "a_i == b_i");
			ensuref(!seen.count({a,b}) && !seen.count({b,a}), "Duplicate edge");
			seen.insert({a,b});
			adj[a].push_back(b);
			adj[b].push_back(a);
			inf.readEoln();
		}
		inf.readEof();
	}
};

#endif
