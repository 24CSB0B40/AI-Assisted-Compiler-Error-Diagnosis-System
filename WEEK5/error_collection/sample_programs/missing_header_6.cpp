// Missing Header Include #6
// Missing #include <cstring>
#include <iostream>
using namespace std;

int main() {
    char str1[20] = "Hello";
    char str2[20];
    strcpy(str2, str1);  // strcpy not declared
    cout << str2 << endl;
    return 0;
}
