/******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************/

// I'm a comment line.
#include <iostream>

/**
 * Say Hello! to the world.
 */
void helloWorld() {
	std::cout << "Hello World!" << std::endl;
}

int main() { // I'm a mixed code-comment line (counted as code).

	// I'm a comment line as well.
	helloWorld();
	return 0;
}
