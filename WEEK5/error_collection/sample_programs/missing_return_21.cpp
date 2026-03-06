// Missing Return Statement #21
#include <iostream>
using namespace std;
bool isPrime(int n) {
    if(n < 2) return false;
    for(int i = 2; i < n; i++) {
        if(n % i == 0) return false;
    }
    // Missing return true
}
int main() {
    cout << isPrime(7) << endl;
    return 0;
}
