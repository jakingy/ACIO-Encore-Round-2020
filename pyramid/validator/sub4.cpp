#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(all_of(c.ai+2, c.ai+c.N+1, [](double ai){return ai == 0;}), "ai != 0.");
	return 0;
}
