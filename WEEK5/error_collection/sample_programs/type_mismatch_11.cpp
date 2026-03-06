// Type Mismatch #11
#include <iostream>
using namespace std;

int main() {
    void *ptr;
    int x = 10;
    int y = ptr;  // Assigning void pointer to int
    cout << y << endl;
    return 0;
}
