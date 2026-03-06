// Invalid Syntax in Declarations #25
#include <iostream>
using namespace std;
int main() {
    shrot s = 100;  // Typo: 'shrot' instead of 'short'
    cout << s << endl;
    return 0;
}
