// Type Mismatch #7
#include <iostream>
using namespace std;

int main() {
    float f;
    f = 'A';  // Assigning char to float (may work but semantically wrong)
    int x = "text";  // Clear type mismatch
    cout << x << endl;
    return 0;
}
