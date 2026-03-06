// Type Mismatch #27
#include <iostream>
using namespace std;
int main() {
    float f;
    f = "pi";  // string to float
    cout << f << endl;
    return 0;
}
