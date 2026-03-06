// Unmatched Braces #28
#include <iostream>
using namespace std;
int main() {
    bool found = false;
    for(int i = 0; i < 10; i++) {
        if(i == 5) {
            found = true;
        // Missing closing brace for if
    }
    cout << found << endl;
    return 0;
}
