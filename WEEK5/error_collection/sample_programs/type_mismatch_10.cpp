// Type Mismatch #10
#include <iostream>
using namespace std;

int main() {
    const char *str = "Hello";
    int num = str;  // Assigning pointer to int
    cout << num << endl;
    return 0;
}
