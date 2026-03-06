// Missing Return Statement #29
#include <iostream>
using namespace std;
bool isEven(int n) {
    if(n % 2 == 0) {
        return true;
    }
    // Missing return false
}
int main() {
    cout << isEven(3) << endl;
    return 0;
}
