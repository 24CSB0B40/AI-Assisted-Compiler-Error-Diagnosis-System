// Type Mismatch #28
#include <iostream>
using namespace std;
int main() {
    short s;
    s = "short_string";  // string to short
    cout << s << endl;
    return 0;
}
