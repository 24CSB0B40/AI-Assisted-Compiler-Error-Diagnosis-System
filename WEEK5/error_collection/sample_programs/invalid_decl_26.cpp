// Invalid Syntax in Declarations #26
#include <iostream>
using namespace std;
int main() {
    Void *ptr = nullptr;  // Wrong case: 'Void'
    cout << ptr << endl;
    return 0;
}
