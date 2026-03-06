// Invalid Syntax in Declarations #22
#include <iostream>
using namespace std;
int main() {
    CONST int MAX = 50;  // Wrong case: 'CONST'
    cout << MAX << endl;
    return 0;
}
