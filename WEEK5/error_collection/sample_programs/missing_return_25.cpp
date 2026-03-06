// Missing Return Statement #25
#include <iostream>
using namespace std;
double power(double base, int exp) {
    double result = 1.0;
    for(int i = 0; i < exp; i++) result *= base;
    // Missing return
}
int main() {
    cout << power(2.0, 8) << endl;
    return 0;
}
