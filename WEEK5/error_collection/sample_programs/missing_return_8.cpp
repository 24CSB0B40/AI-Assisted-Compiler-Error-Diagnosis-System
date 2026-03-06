// Missing Return Statement #8
#include <iostream>
using namespace std;

string getMessage() {
    string msg = "Hello World";
    // Missing return statement
}

int main() {
    cout << getMessage() << endl;
    return 0;
}
