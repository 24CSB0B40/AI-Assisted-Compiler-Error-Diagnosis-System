// Unmatched Braces #27
#include <iostream>
using namespace std;
int main() {
    int x = 10;
    {
        int y = x * 2;
        cout << y << endl;
    // Missing closing brace for block
    return 0;
}
