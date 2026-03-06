// Missing Return Statement #14
#include <iostream>
using namespace std;
int triple(int x) {
    int result = x * 3;
    // Missing return
}
int main() {
    cout << triple(4) << endl;
    return 0;
}
