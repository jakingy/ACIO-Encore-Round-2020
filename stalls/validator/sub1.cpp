#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(c.S*(c.S-1)/2 == c.R, "Graph is not a complete graph.");
	return 0;
}
