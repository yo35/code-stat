/******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************/

// I'm a comment line.

/**
 * Say Hello! to the world.
 */
function helloWorld() {
	console.log('Hello World!');
}

if (require.main === module) { // I'm a mixed code-comment line (counted as code).

	// I'm a comment line as well.
	helloWorld();
}
