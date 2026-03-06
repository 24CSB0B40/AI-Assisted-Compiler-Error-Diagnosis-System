// Unmatched Braces #3
#include <iostream>
using namespace std;

int main() {
    int x = 10;
    {
        int y = 20;
        cout << x + y << endl;
    // Missing closing brace for inner block
    return 0;
}
