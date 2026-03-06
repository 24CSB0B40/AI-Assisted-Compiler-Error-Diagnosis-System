// Missing Header Include #20
// Missing #include <sstream>
#include <iostream>
using namespace std;
int main() {
    stringstream ss;  // stringstream not declared
    ss << 42;
    cout << ss.str() << endl;
    return 0;
}
