// Invalid Syntax in Declarations #23
#include <iostream>
using namespace std;
int main() {
    lng long bigNum = 99999;  // Typo: 'lng' instead of 'long'
    cout << bigNum << endl;
    return 0;
}
