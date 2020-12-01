#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(c.M == 3, "M != 3.");
	ensuref(c.C == 2, "C != 2.");
	ensuref(all_of(c.p.begin()+1, c.p.begin()+c.S+1, [](int p){return p == 1 || p == 2;}), "p_i is not 1 or 2.");
	return 0;
}
