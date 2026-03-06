// Missing Header Include #17
// Missing #include <queue>
#include <iostream>
using namespace std;
int main() {
    queue<int> q;  // queue not declared
    q.push(5);
    cout << q.front() << endl;
    return 0;
}
