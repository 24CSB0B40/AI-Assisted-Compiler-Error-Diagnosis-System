// Missing Return Statement #10
#include <iostream>
using namespace std;

float average(int a, int b) {
    float avg = (a + b) / 2.0;
    cout << "Average: " << avg << endl;
    // Missing return statement
}

int main() {
    cout << average(10, 20) << endl;
    return 0;
}
