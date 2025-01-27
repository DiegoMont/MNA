#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

const int N = 1000000;

void printArraySubset(int* array, const char* arrayName) {
    const int MAX_ELEMENTS_TO_PRINT = 10;
    printf("%s: ", arrayName);
    for (int i = 0; i < MAX_ELEMENTS_TO_PRINT; i++)
        printf("%d  ", array[i]);
    printf("\n");
}

void fillRandomly(int* array) {
    for (int i = 0; i < N; i++)
        array[i] = rand() % 100;
}

int main() {
    int *a = new int[N], *b = new int[N], *c = new int[N];
    fillRandomly(a);
    fillRandomly(b);

    #pragma omp parallel for shared(c)
    for (int i = 0; i < N; i++)
        c[i] = a[i] + b[i];

    printArraySubset(a, "A");
    printArraySubset(b, "B");
    printArraySubset(c, "C");
}
