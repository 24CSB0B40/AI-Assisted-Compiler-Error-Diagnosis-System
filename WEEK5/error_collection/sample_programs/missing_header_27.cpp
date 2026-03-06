// Missing Header Include #27
// Missing #include <list>
#include <iostream>
using namespace std;
int main() {
    list<int> lst;  // list not declared
    lst.push_back(1);
    cout << lst.front() << endl;
    return 0;
}
