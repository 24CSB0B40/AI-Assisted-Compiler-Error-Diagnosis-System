// Missing Return Statement #13
#include <iostream>
using namespace std;

int count(int arr[], int size) {
    int c = 0;
    for(int i = 0; i < size; i++) {
        if(arr[i] > 0) {
            c++;
        }
    }
    // Missing return statement
}

int main() {
    int nums[] = {1, -2, 3, -4, 5};
    cout << count(nums, 5) << endl;
    return 0;
}
