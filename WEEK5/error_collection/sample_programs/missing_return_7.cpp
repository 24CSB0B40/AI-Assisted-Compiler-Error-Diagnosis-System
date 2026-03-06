// Missing Return Statement #7
#include <iostream>
using namespace std;

int max(int a, int b) {
    if(a > b) {
        return a;
    }
    // Missing return for a <= b case
}

int main() {
    cout << max(3, 7) << endl;
    return 0;
}
