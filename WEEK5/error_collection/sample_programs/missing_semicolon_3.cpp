// Missing Semicolon #3
#include <iostream>
using namespace std;

int main() {
    float price = 99.99  // Missing semicolon
    float tax = price * 0.1;
    cout << "Total: " << price + tax << endl;
    return 0;
}
