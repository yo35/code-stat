/******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************/

// I'm a comment line.
using System;

class ProgramHelloWorld {

    /**
     * Say Hello! to the world.
     */
    private static void helloWorld() {
        Console.WriteLine("Hello World!");
    }

    static void Main(string[] args) { // I'm a mixed code-comment line (counted as code).

        // I'm a comment line as well.
        helloWorld();
    }

}
