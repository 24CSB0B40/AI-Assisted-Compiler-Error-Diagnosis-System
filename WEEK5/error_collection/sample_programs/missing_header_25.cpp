// Missing Header Include #25
// Missing #include <cmath>
#include <iostream>
using namespace std;
int main() {
    double r = ceil(3.2);  // ceil not declared
    cout << r << endl;
    return 0;
}
