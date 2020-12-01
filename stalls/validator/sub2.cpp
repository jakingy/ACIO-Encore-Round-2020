#include "common.h"

int main() {
	Checker c{}; c.validate();
	ensuref(c.S <= 16, "S > 16.");
	return 0;
}
