// Unmatched Parentheses #27
#include <iostream>
using namespace std;
int main() {
    int a = 2, b = 3, c = 4;
    int sum = (a + (b + c);  // Missing closing paren
    cout << sum << endl;
    return 0;
}
