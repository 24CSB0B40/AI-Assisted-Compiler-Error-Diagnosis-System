// Type Mismatch #15
#include <iostream>
using namespace std;
int main() {
    int x = 3.14;  // implicit narrowing (error in strict mode)
    char *p = x;   // int to pointer
    cout << p << endl;
    return 0;
}
