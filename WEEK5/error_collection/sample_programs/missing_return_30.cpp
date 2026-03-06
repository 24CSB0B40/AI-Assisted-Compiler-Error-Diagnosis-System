// Missing Return Statement #30
#include <iostream>
using namespace std;
int cube(int x) {
    int c = x * x * x;
    cout << "Cube calculated" << endl;
    // Missing return
}
int main() {
    cout << cube(3) << endl;
    return 0;
}
