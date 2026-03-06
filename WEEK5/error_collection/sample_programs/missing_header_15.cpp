// Missing Header Include #15
// Missing #include <cctype>
#include <iostream>
using namespace std;

int main() {
    char ch = 'a';
    char upper = toupper(ch);  // toupper not declared
    cout << upper << endl;
    return 0;
}
