// Missing Semicolon #12
#include <iostream>
using namespace std;

int main() {
    int *ptr = nullptr  // Missing semicolon
    int value = 42;
    ptr = &value;
    cout << *ptr << endl;
    return 0;
}
