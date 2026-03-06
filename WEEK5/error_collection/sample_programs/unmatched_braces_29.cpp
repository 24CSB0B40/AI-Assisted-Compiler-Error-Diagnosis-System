// Unmatched Braces #29
#include <iostream>
using namespace std;
int main() {
    int n = 3;
    while(n > 0) {
        cout << n << endl;
        n--;
    // Missing closing brace for while
    cout << "Done" << endl;
    return 0;
}
