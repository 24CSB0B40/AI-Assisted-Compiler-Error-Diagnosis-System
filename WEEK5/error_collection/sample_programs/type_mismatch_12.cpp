// Type Mismatch #12
#include <iostream>
using namespace std;

int main() {
    short s;
    string text = "number";
    s = text;  // Assigning string to short
    cout << s << endl;
    return 0;
}
