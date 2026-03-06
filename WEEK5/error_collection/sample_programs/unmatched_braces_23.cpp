// Unmatched Braces #23
#include <iostream>
using namespace std;
int main() {
    int x = 5;
    switch(x) {
        case 5:
            cout << "Five" << endl;
            break;
        default:
            cout << "Other" << endl;
    // Missing closing brace for switch
    return 0;
}
