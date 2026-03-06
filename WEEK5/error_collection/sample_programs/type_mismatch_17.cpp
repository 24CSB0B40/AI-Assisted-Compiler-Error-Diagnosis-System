// Type Mismatch #17
#include <iostream>
using namespace std;
int main() {
    bool b = "yes";  // string to bool
    cout << b << endl;
    return 0;
}
