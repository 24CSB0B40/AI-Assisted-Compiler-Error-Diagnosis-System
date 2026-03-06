// Missing Return Statement #26
#include <iostream>
using namespace std;
int gcd(int a, int b) {
    while(b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    // Missing return
}
int main() {
    cout << gcd(12, 8) << endl;
    return 0;
}
