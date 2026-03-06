// Missing Semicolon #2
#include <iostream>
using namespace std;

int main() {
    int a = 5;
    int b = 10  // Missing semicolon
    int c = a + b;
    cout << c << endl;
    return 0;
}
