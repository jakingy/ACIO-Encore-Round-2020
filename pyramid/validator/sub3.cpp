#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(all_of(c.ai+2, c.ai+c.N+1, [](double ai){return ai == 0;}), "ai != 0.");
	for (int i = 3; i <= c.N; ++i) {
		ensuref(c.bi[i-1] >= c.bi[i], "i < j, but bi < bj.");
	}
	return 0;
}
