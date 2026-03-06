// Undeclared Variable #3
#include <iostream>
using namespace std;

int main() {
    sum = 0;  // 'sum' not declared
    for(int i = 0; i < 10; i++) {
        sum += i;
    }
    cout << sum << endl;
    return 0;
}
