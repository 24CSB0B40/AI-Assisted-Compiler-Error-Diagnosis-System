// Missing Header Include #30
// Missing #include <bitset>
#include <iostream>
using namespace std;
int main() {
    bitset<8> b(255);  // bitset not declared
    cout << b << endl;
    return 0;
}
