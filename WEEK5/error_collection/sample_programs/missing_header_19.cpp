// Missing Header Include #19
// Missing #include <cmath>
#include <iostream>
using namespace std;
int main() {
    double x = fabs(-5.5);  // fabs not declared
    cout << x << endl;
    return 0;
}
