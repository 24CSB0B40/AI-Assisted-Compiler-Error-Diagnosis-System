// Type Mismatch #5
#include <iostream>
using namespace std;

int main() {
    int *ptr;
    ptr = 123;  // Assigning int to pointer
    cout << ptr << endl;
    return 0;
}
