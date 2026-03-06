// Missing Header Include #4
// Missing #include <vector>
#include <iostream>
using namespace std;

int main() {
    vector<int> nums;  // vector not declared
    nums.push_back(10);
    cout << nums[0] << endl;
    return 0;
}
