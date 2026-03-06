// Unmatched Braces #22
#include <iostream>
using namespace std;
int main() {
    int score = 75;
    if(score >= 90) {
        cout << "A" << endl;
    } else if(score >= 80) {
        cout << "B" << endl;
    } else {
        cout << "C" << endl;
    // Missing closing brace for else
    return 0;
}
