#ifndef COMMON_H
#define COMMON_H
#include "testlib.h"
#include "bounds.h"
using namespace std;

struct Checker {
	int H, Q, N, X[MAX_Q];
	double R[MAX_Q], ai[MAX_N], bi[MAX_N];
	void validate() {
		registerValidation();
		H = inf.readInt(MIN_H, MAX_H, "H");
		inf.readEoln();
		N = (1<<H) - 1;
		for (int i = 2; i <= N; i++) {
			ai[i] = inf.readDouble(MIN_R, MAX_R, "ai"); // this doesn't check 6 decimal places
			inf.readSpace();
			bi[i] = inf.readDouble(MIN_R, MAX_R, "bi");
			ensuref(ai[i] <= bi[i], "ai > bi");
			inf.readEoln();
		}
		Q = inf.readInt(MIN_Q, MAX_Q, "Q");
		inf.readEoln();
		for (int q = 0; q < Q; q++) {
			X[q] = inf.readInt(1, N, "X");
			inf.readSpace();
			R[q] = inf.readDouble(MIN_R, MAX_R, "R");
			inf.readEoln();
		}
		inf.readEof();
	}
};

#endif
