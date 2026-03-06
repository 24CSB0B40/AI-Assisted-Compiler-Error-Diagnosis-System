// Invalid Syntax in Declarations #12
#include <iostream>
using namespace std;

int main() {
    cosnt int MAX = 100;  // Typo: 'cosnt' instead of 'const'
    cout << MAX << endl;
    return 0;
}
