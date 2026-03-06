// Missing Return Statement #5
#include <iostream>
using namespace std;

char getGrade(int marks) {
    if(marks >= 90) {
        return 'A';
    }
    if(marks >= 80) {
        return 'B';
    }
    // Missing return for marks < 80
}

int main() {
    cout << getGrade(75) << endl;
    return 0;
}
