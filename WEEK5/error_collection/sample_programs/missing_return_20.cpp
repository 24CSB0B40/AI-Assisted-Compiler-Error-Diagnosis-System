// Missing Return Statement #20
#include <iostream>
using namespace std;
int sumDigits(int n) {
    int s = 0;
    while(n > 0) {
        s += n % 10;
        n /= 10;
    }
    // Missing return
}
int main() {
    cout << sumDigits(123) << endl;
    return 0;
}
