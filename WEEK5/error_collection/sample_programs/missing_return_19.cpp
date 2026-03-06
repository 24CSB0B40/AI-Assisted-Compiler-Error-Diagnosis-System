// Missing Return Statement #19
#include <iostream>
using namespace std;
float divide(float a, float b) {
    if(b != 0) {
        return a / b;
    }
    // Missing return for b == 0
}
int main() {
    cout << divide(10, 0) << endl;
    return 0;
}
