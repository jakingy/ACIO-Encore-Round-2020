#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(all_of(c.R, c.R+c.Q, [&](double R){return R == c.R[0];}), "R is not the same for all queries.");
	return 0;
}
