// Type Mismatch #14
#include <iostream>
using namespace std;
int main() {
    float f = "hello";  // string to float
    cout << f << endl;
    return 0;
}
