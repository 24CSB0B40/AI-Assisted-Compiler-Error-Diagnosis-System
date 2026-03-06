// Missing Return Statement #16
#include <iostream>
using namespace std;
int min_val(int a, int b) {
    if(a < b) {
        return a;
    }
    // Missing return for a >= b
}
int main() {
    cout << min_val(3, 7) << endl;
    return 0;
}
