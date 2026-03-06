// Type Mismatch #19
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    s = 3.14;  // double to string
    cout << s << endl;
    return 0;
}
