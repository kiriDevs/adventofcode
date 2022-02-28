#include <iostream>
#include <fstream>

using namespace std;

int main() {
  ifstream infile ("../input");
  int inputNumbers[2000];

  int curInNumber; 
  int curInLineInx = -1;
  while (infile >> curInNumber) {
    curInLineInx += 1;
    inputNumbers[curInLineInx] = curInNumber;
  }

  int wentDeeperTimes = 0;
  int prevNum = inputNumbers[0];
  for (int i = 1; i < 2000; i++) {
    int curNum = inputNumbers[i];
    if (curNum > prevNum) {
      wentDeeperTimes += 1;
    }
    prevNum = curNum;
  }

  cout << wentDeeperTimes << endl;
}
