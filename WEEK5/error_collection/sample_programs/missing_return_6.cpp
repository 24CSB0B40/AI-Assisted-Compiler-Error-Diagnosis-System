// Missing Return Statement #6
#include <iostream>
using namespace std;

int sum(int a, int b) {
    int result = a + b;
    cout << "Sum calculated" << endl;
    // Missing return statement
}

int main() {
    cout << sum(5, 10) << endl;
    return 0;
}
