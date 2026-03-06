// Missing Header Include #8
// Missing #include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums = {3, 1, 4, 1, 5};
    sort(nums.begin(), nums.end());  // sort not declared
    cout << nums[0] << endl;
    return 0;
}
