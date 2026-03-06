// Unmatched Braces #26
#include <iostream>
using namespace std;
int main() {
    int arr[] = {1, 2, 3, 4, 5;  // Missing closing brace in array init
    for(int i = 0; i < 5; i++) {
        cout << arr[i] << endl;
    }
    return 0;
}
