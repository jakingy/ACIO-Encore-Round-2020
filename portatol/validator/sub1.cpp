#include "common.h"

int main() {
	Checker c{}; c.validate();
	for (int n = 0; n < c.N; n++) {
		for (int m = 0; m < c.M; m++) {
			ensuref(c.grid[n][m] != 'T', "Teleporter squares not allowed in sub1.");
		}
	}
	return 0;
}
