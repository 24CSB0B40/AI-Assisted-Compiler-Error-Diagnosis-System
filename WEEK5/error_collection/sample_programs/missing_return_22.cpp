// Missing Return Statement #22
#include <iostream>
using namespace std;
int clamp(int val, int lo, int hi) {
    if(val < lo) return lo;
    if(val > hi) return hi;
    // Missing return val
}
int main() {
    cout << clamp(5, 1, 10) << endl;
    return 0;
}
