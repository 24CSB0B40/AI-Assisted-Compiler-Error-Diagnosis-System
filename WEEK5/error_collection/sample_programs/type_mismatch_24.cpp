// Type Mismatch #24
#include <iostream>
using namespace std;
int main() {
    int arr[3] = {1,2,3};
    double d = arr;  // array to double
    cout << d << endl;
    return 0;
}
