// Missing Return Statement #28
#include <iostream>
using namespace std;
int reverseNum(int n) {
    int rev = 0;
    while(n != 0) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    // Missing return
}
int main() {
    cout << reverseNum(1234) << endl;
    return 0;
}
