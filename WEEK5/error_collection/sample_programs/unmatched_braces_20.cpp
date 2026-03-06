// Unmatched Braces #20
#include <iostream>
using namespace std;
int main() {
    int x = 10;
    if(x > 0) {
        if(x > 5) {
            cout << "Big" << endl;
        }
    // Missing closing brace for outer if
    return 0;
}
