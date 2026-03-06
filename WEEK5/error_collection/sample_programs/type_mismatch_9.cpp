// Type Mismatch #9
#include <iostream>
using namespace std;

int main() {
    int numbers[3] = {1, 2, 3};
    int single = numbers;  // Assigning array to int
    cout << single << endl;
    return 0;
}
