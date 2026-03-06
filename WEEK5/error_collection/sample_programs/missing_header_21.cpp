// Missing Header Include #21
// Missing #include <cstring>
#include <iostream>
using namespace std;
int main() {
    char s[] = "hello";
    int len = strlen(s);  // strlen not declared
    cout << len << endl;
    return 0;
}
