// Missing Semicolon #11
#include <iostream>
using namespace std;

int main() {
    int count = 0  // Missing semicolon
    while(count < 3) {
        cout << count << endl;
        count++;
    }
    return 0;
}
