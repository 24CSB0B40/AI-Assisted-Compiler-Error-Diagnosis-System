// Missing Header Include #23
// Missing #include <cstdlib>
#include <iostream>
using namespace std;
int main() {
    int n = abs(-10);  // abs not declared
    cout << n << endl;
    return 0;
}
