#include "common.h"

int depth(int x){
    return 31-__builtin_clz(x);
}

int main() {
	Checker c{}; c.validate();
	ensuref(c.H >= 2, "H < 2.");
	ensuref(all_of(c.X, c.X+c.Q, [&c](int X){return depth(X) == c.H-2;}), "X is not at a depth of H - 2.");
	return 0;
}
