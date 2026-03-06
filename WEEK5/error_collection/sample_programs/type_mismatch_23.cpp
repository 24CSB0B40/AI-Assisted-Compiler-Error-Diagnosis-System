// Type Mismatch #23
#include <iostream>
using namespace std;
int main() {
    void *vp;
    int x = vp;  // void pointer to int
    cout << x << endl;
    return 0;
}
