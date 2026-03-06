// Missing Return Statement #9
#include <iostream>
using namespace std;

int factorial(int n) {
    if(n <= 1) {
        return 1;
    }
    int result = n * factorial(n - 1);
    // Missing return statement
}

int main() {
    cout << factorial(5) << endl;
    return 0;
}
