/******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************/

package com.yo35.codestat;

// I'm a comment line.

public class ProgramHelloWorld {

	/**
	 * Say Hello! to the world.
	 */
	private static void helloWorld() {
		System.out.println("Hello World!");
	}

	public static void main(String[] args) { // I'm a mixed code-comment line (counted as code).

		// I'm a comment line as well.
		helloWorld();
	}

}
