// minimal example on using host device functions
// compile with:
// nvcc -o hostDev main.cu

#include <iostream>
#include <stdio.h>

// CUDA global constants
__constant__ __device__ int32_t dconst = 5;
const int32_t hconst = 10;

__host__ __device__ void foo(){
    #ifdef __CUDA_ARCH__
        printf("%d \n", dconst);
    #else
        printf("%d \n", hconst);
    #endif
}

__global__ void fooKernel(){
    printf("Hello from block %d, thread %d\n", blockIdx.x, threadIdx.x);
    foo();
}

int main()
{
    // Kernel invocation with N threads

    std::cout << "run the cuda kernel" << std::endl;
    fooKernel<<<1, 4>>>();
    cudaDeviceSynchronize();

    std::cout << "run the host function" << std::endl;
    foo();

    return 0;

}