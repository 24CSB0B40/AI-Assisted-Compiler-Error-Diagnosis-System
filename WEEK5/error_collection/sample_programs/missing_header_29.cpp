// Missing Header Include #29
// Missing #include <utility>
#include <iostream>
using namespace std;
int main() {
    pair<int, int> p = make_pair(3, 4);  // pair not declared
    cout << p.first << endl;
    return 0;
}
