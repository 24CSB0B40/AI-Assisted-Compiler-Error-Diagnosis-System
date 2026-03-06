// Type Mismatch #8
#include <iostream>
using namespace std;

int main() {
    double d;
    char text[] = "hello";
    d = text;  // Assigning char array to double
    cout << d << endl;
    return 0;
}
