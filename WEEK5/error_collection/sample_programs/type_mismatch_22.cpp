// Type Mismatch #22
#include <iostream>
using namespace std;
int main() {
    int x = 5;
    int y = 2;
    string result = x / y;  // int to string
    cout << result << endl;
    return 0;
}
