// Missing Header Include #7
// Missing #include <ctime>
#include <iostream>
using namespace std;

int main() {
    time_t now = time(0);  // time not declared
    cout << now << endl;
    return 0;
}
