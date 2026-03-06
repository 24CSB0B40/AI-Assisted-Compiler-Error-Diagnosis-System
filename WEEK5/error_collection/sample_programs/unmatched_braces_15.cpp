// Unmatched Braces #15
#include <iostream>
using namespace std;
int main() {
    for(int i = 0; i < 3; i++) 
        cout << i << endl;
    
    if(true) {
        cout << "Yes" << endl;
    // Missing closing brace
    return 0;
}
