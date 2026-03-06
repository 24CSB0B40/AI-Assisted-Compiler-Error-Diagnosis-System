// Type Mismatch #21
#include <iostream>
using namespace std;
int main() {
    long l;
    l = "bignum";  // string to long
    cout << l << endl;
    return 0;
}
