// Missing Header Include #22
// Missing #include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
int main() {
    vector<int> v = {5, 1, 4, 2};
    reverse(v.begin(), v.end());  // reverse not declared
    cout << v[0] << endl;
    return 0;
}
