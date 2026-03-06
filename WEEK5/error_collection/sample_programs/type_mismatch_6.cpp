// Type Mismatch #6
#include <iostream>
using namespace std;

int main() {
    string name;
    name = 42;  // Assigning int to string
    cout << name << endl;
    return 0;
}
