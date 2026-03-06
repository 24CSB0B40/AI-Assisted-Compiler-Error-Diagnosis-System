// Missing Header Include #28
// Missing #include <tuple>
#include <iostream>
using namespace std;
int main() {
    tuple<int, string> t = make_tuple(1, "one");  // tuple not declared
    cout << get<0>(t) << endl;
    return 0;
}
