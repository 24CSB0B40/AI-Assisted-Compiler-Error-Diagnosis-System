// Missing Header Include #10
// Missing #include <fstream>
#include <iostream>
using namespace std;

int main() {
    ofstream file("test.txt");  // ofstream not declared
    file << "Hello File" << endl;
    file.close();
    return 0;
}
