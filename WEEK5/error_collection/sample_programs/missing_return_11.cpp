// Missing Return Statement #11
#include <iostream>
using namespace std;

int absolute(int num) {
    if(num >= 0) {
        return num;
    } else {
        return -num;
    }
    // Actually has return, but compiler might complain about control flow
}

int square(int x) {
    x = absolute(x);
    int sq = x * x;
    // Missing return
}

int main() {
    cout << square(-5) << endl;
    return 0;
}
