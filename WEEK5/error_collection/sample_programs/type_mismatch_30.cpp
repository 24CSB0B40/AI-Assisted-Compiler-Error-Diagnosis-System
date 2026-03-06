// Type Mismatch #30
#include <iostream>
using namespace std;
int main() {
    double d = 9.99;
    int *p = d;  // double to int pointer
    cout << p << endl;
    return 0;
}
