// Missing Return Statement #17
#include <iostream>
using namespace std;
string classify(int n) {
    if(n > 0) return "positive";
    if(n < 0) return "negative";
    // Missing return for n == 0
}
int main() {
    cout << classify(0) << endl;
    return 0;
}
