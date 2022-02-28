#include <iostream>
#include <fstream>
#include <string>

using namespace std;

const string SPACE = " ";

int depth = 0;
int horizontal = 0;

void up(int a) { depth -= a; }
void down(int a) { depth += a; }
void forward(int a) { horizontal += a; }

void interpretStatement(string instruction, int number) {
  if (instruction == "up") up(number);
  else if (instruction == "down") down(number);
  else if (instruction == "forward") forward(number);
  else cout << "WARN: Skipping " << instruction << "::" << number << endl;
}

int main() {
  ifstream inFile ("../input");
  string curLine;
  while(getline(inFile, curLine)) {
    int spaceInx = curLine.find(SPACE);

    string instruction = curLine.substr(0, spaceInx);
    int number = stoi(curLine.substr(spaceInx));

    interpretStatement(instruction, number);
  }

  int solution = depth * horizontal;
  cout << solution << endl;
}
