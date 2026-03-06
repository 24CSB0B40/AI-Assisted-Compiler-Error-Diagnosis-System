// Missing Semicolon #7
#include <iostream>
using namespace std;

int main() {
    bool flag = true  // Missing semicolon
    if(flag) {
        cout << "Flag is true" << endl;
    }
    return 0;
}
