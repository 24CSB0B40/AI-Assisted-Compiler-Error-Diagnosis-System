// Type Mismatch #26
#include <iostream>
#include <string>
using namespace std;
int main() {
    string name = "Alice";
    int n = name;  // string to int
    cout << n << endl;
    return 0;
}
