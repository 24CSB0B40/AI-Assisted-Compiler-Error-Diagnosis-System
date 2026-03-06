// Missing Return Statement #1
#include <iostream>
using namespace std;

int calculate(int x) {
    if(x > 0) {
        return x * 2;
    }
    // Missing return for x <= 0 case
}

int main() {
    cout << calculate(5) << endl;
    return 0;
}
