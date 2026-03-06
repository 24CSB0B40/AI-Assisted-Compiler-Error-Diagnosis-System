// Unmatched Braces #17
#include <iostream>
using namespace std;
int main() {
    {
        int a = 5;
        {
            int b = 10;
            cout << a + b << endl;
        // Missing one closing brace
    }
    return 0;
}
