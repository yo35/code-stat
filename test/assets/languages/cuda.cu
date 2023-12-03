/******************************************************************************
 * This is a file header, not counted as comment.                             *
 ******************************************************************************/

// I'm a comment line.
#include <stdio.h>

/**
 * Say Hello! to the world (from a CUDA kernel).
 */
__global__ void helloWorld() {
    printf("Hello World!\n");
}

int main() { // I'm a mixed code-comment line (counted as code).
    helloWorld<<< 1, 1 >>>();
    cudaDeviceSynchronize();
    return 0;
}
