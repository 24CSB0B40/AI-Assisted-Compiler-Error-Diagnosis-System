// Unmatched Braces #10
#include <iostream>
using namespace std;

int main() {
    if(true) {
        if(true) {
            cout << "Nested" << endl;
        }
    // Missing closing brace for outer if
    return 0;
}
