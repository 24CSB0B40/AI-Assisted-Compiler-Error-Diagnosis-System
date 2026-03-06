// Missing Return Statement #12
#include <iostream>
using namespace std;

long power(int base, int exp) {
    long result = 1;
    for(int i = 0; i < exp; i++) {
        result *= base;
    }
    // Missing return statement
}

int main() {
    cout << power(2, 3) << endl;
    return 0;
}
