// Missing Return Statement #2
#include <iostream>
using namespace std;

int getValue() {
    int x = 10;
    // Missing return statement
}

int main() {
    cout << getValue() << endl;
    return 0;
}
