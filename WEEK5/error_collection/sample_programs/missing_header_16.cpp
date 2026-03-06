// Missing Header Include #16
// Missing #include <set>
#include <iostream>
using namespace std;
int main() {
    set<int> s;  // set not declared
    s.insert(10);
    cout << *s.begin() << endl;
    return 0;
}
