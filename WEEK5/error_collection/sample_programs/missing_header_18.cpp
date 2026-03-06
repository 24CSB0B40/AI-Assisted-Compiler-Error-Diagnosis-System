// Missing Header Include #18
// Missing #include <stack>
#include <iostream>
using namespace std;
int main() {
    stack<int> st;  // stack not declared
    st.push(10);
    cout << st.top() << endl;
    return 0;
}
