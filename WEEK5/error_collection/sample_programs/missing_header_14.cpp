// Missing Header Include #14
// Missing #include <map>
#include <iostream>
using namespace std;

int main() {
    map<string, int> ages;  // map not declared
    ages["Alice"] = 25;
    cout << ages["Alice"] << endl;
    return 0;
}
