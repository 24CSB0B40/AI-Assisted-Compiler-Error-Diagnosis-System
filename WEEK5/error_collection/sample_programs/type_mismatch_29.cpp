// Type Mismatch #29
#include <iostream>
using namespace std;
int main() {
    int x = 10;
    char *c = x;  // int to char pointer
    cout << c << endl;
    return 0;
}
