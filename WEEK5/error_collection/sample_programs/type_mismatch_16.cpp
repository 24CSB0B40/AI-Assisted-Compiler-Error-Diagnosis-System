// Type Mismatch #16
#include <iostream>
using namespace std;
int main() {
    int *p;
    p = "text";  // string literal to int pointer
    cout << p << endl;
    return 0;
}
