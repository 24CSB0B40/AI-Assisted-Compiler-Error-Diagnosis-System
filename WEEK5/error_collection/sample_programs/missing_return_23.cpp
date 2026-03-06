// Missing Return Statement #23
#include <iostream>
using namespace std;
long long factorial(int n) {
    if(n == 0) return 1;
    long long result = n * factorial(n-1);
    // Missing return
}
int main() {
    cout << factorial(5) << endl;
    return 0;
}
