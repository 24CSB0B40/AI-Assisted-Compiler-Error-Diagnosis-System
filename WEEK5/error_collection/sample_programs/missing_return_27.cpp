// Missing Return Statement #27
#include <iostream>
using namespace std;
char letterGrade(int marks) {
    if(marks >= 90) return 'A';
    if(marks >= 75) return 'B';
    if(marks >= 60) return 'C';
    // Missing return for marks < 60
}
int main() {
    cout << letterGrade(50) << endl;
    return 0;
}
