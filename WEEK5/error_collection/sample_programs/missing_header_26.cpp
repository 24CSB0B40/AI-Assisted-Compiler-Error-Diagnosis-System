// Missing Header Include #26
// Missing #include <map>
#include <iostream>
using namespace std;
int main() {
    map<int, string> m;  // map not declared
    m[1] = "one";
    cout << m[1] << endl;
    return 0;
}
