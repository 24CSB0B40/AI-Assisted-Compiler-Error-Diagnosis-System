// Unmatched Braces #16
#include <iostream>
using namespace std;
int helper() {
    int x = 10;
    return x;
// Missing closing brace for function

int main() {
    cout << helper() << endl;
    return 0;
}
