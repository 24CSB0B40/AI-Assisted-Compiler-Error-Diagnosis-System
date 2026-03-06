// Missing Return Statement #24
#include <iostream>
using namespace std;
int countPositives(int arr[], int n) {
    int count = 0;
    for(int i = 0; i < n; i++) {
        if(arr[i] > 0) count++;
    }
    // Missing return
}
int main() {
    int a[] = {1,-2,3,-4,5};
    cout << countPositives(a, 5) << endl;
    return 0;
}
