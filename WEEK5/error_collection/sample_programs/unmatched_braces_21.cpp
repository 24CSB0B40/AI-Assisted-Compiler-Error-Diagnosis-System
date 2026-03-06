// Unmatched Braces #21
#include <iostream>
using namespace std;
int main() {
    for(int i = 0; i < 2; i++) {
        for(int j = 0; j < 2; j++) {
            cout << i+j << endl;
        }
    // Missing closing brace for outer for
    return 0;
}
