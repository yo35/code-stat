/******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************/

// I'm a comment line.
#include <stdio.h>

/**
 * Say Hello! to the world.
 */
void helloWorld() {
	printf("Hello World!\n");
}

int main() { // I'm a mixed code-comment line (counted as code).

	// I'm a comment line as well.
	helloWorld();
	return 0;
}
