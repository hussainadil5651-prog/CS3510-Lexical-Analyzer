/* Sample C Program for Lexical Analysis */
#include <stdio.h>

#define MAX 100

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

float calculate_average(int arr[], int size) {
    int sum = 0;
    float avg;

    for (int i = 0; i < size; i++) {
        sum = sum + arr[i];
    }

    avg = (float)sum / size;
    return avg;
}

int main() {
    int numbers[5];
    int x = 42;
    float result;
    char grade = 'A';

    // Initialize array
    numbers[0] = 10;
    numbers[1] = 20;
    numbers[2] = 30;
    numbers[3] = 40;
    numbers[4] = 50;

    result = calculate_average(numbers, 5);

    if (result > 25) {
        printf("Above average: %f\n", result);
    } else {
        printf("Below average: %f\n", result);
    }

    return 0;
}
