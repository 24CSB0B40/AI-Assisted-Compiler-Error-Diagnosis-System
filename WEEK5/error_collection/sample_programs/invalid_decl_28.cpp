// Invalid Syntax in Declarations #28
#include <iostream>
using namespace std;
int main() {
    long long long x = 5;  // Triple long is invalid
    cout << x << endl;
    return 0;
}
