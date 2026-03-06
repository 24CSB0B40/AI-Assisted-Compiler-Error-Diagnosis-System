// Missing Return Statement #3
#include <iostream>
using namespace std;

double getPrice() {
    double price = 99.99;
    cout << "Price calculated" << endl;
    // Missing return statement
}

int main() {
    cout << getPrice() << endl;
    return 0;
}
