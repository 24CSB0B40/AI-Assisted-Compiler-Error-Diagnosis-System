// Type Mismatch #25
#include <iostream>
using namespace std;
int main() {
    char *cp;
    int num = cp;  // char pointer to int
    cout << num << endl;
    return 0;
}
