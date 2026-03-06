// Missing Header Include #13
// Missing #include <limits>
#include <iostream>
using namespace std;

int main() {
    int maxInt = numeric_limits<int>::max();  // numeric_limits not declared
    cout << maxInt << endl;
    return 0;
}
