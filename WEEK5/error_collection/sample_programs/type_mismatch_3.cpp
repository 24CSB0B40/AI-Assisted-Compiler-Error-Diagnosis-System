// Type Mismatch #3
#include <iostream>
using namespace std;

int main() {
    int arr[5];
    arr = 10;  // Assigning int to array
    cout << arr[0] << endl;
    return 0;
}
