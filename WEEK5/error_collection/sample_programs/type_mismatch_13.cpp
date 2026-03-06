// Type Mismatch #13
#include <iostream>
using namespace std;

int main() {
    int x = 5;
    int y = 10;
    string result = x + y;  // Assigning int sum to string
    cout << result << endl;
    return 0;
}
