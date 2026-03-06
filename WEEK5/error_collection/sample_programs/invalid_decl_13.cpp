// Invalid Syntax in Declarations #13
#include <iostream>
using namespace std;

int main() {
    unsignd int positive = 50;  // Typo: 'unsignd' instead of 'unsigned'
    cout << positive << endl;
    return 0;
}
