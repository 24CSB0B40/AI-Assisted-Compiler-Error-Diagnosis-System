// Unmatched Braces #11
#include <iostream>
using namespace std;

int main() {
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            cout << i << "," << j << endl;
        // Missing closing brace for inner for
    }
    return 0;
}
