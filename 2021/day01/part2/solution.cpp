#include <iostream>
#include <fstream>

using namespace std;

const int windowSize = 3;
int window[windowSize];

void shiftWindow(int newValue) {
  window[0] = window[1];
  window[1] = window[2];
  window[2] = newValue;
}

int windowTotal() {
  int ret = 0;
  for (int i = 0; i < windowSize; i++) ret += window[i];
  return ret;
}

int main() {
  ifstream inFile ("../input");
  int inputNumbers[2000];

  int curInNumber;
  int curInLineInx = -1;
  while (inFile >> curInNumber) {
    curInLineInx += 1;
    inputNumbers[curInLineInx] = curInNumber;
  }

  // Set the first window
  for (int i = 0; i <= windowSize; i++) window[i] = inputNumbers[i];

  int wentDeeperTimes = 0;
  for (int i = 3; i < 2000; i++) {
    int prev = windowTotal();
    shiftWindow(inputNumbers[i]);
    int cur = windowTotal();
    if (cur > prev) wentDeeperTimes += 1;
  }

  cout << wentDeeperTimes << endl;
}


