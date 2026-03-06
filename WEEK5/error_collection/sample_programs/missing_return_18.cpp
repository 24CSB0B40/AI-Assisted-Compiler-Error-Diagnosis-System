// Missing Return Statement #18
#include <iostream>
using namespace std;
int fibonacci(int n) {
    if(n <= 1) return n;
    int a = fibonacci(n-1) + fibonacci(n-2);
    // Missing return
}
int main() {
    cout << fibonacci(6) << endl;
    return 0;
}
