// Missing Header Include #12
// Missing #include <cstdlib>
#include <iostream>
using namespace std;

int main() {
    int r = rand();  // rand not declared
    cout << r << endl;
    return 0;
}
