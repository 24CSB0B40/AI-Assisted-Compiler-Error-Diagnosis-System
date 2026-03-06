// Type Mismatch #20
#include <iostream>
using namespace std;
int main() {
    char arr[10];
    arr = 100;  // int to char array
    cout << arr << endl;
    return 0;
}
