#ifndef COMMON_H
#define COMMON_H
#include "testlib.h"
#include "bounds.h"
using namespace std;

struct Checker {
	int N, M;
	char grid[MAX_N][MAX_N];
	void validate() {
		registerValidation();
		N = inf.readInt(MIN_N, MAX_N, "N");
		inf.readSpace();
		M = inf.readInt(MIN_N, MAX_N, "M");
		inf.readEoln();
		for (int n = 0; n < N; n++) {
			for (int m = 0; m < M; m++) {
				grid[n][m] = inf.readChar();
				ensuref(grid[n][m] == '.' || grid[n][m] == 'P' || grid[n][m] == 'T', "Unknown square type");
			}
			inf.readEoln();	
		}
		ensuref(grid[N-1][M-1] != 'T', "Bottom-right square cannot be a teleporter.");
		inf.readEof();
	}
};

#endif
