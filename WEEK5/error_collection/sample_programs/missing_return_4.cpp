// Missing Return Statement #4
#include <iostream>
using namespace std;

bool isPositive(int num) {
    if(num > 0) {
        return true;
    } else if(num < 0) {
        return false;
    }
    // Missing return for num == 0 case
}

int main() {
    cout << isPositive(0) << endl;
    return 0;
}
