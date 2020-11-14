#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(c.N == 1, "N must be 1 for sub2.");
	int cnt = 0;
	for (int m = 0; m < c.M; m++) {
		if (c.grid[0][m] == 'T') cnt++;
	}
	ensuref(cnt == 1, "There must be exactly 1 teleporter square for sub2.");
	return 0;
}
