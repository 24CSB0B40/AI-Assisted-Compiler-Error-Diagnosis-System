// Unmatched Parentheses #23
#include <iostream>
using namespace std;
int main() {
    bool flag = (true && (false || true);  // Missing closing paren
    cout << flag << endl;
    return 0;
}
