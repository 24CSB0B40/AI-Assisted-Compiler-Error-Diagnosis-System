// Invalid Syntax in Declarations #10
#include <iostream>
using namespace std;

int main() {
    short short int x = 5;  // Duplicate 'short'
    cout << x << endl;
    return 0;
}
