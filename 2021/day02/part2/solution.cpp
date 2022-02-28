#include <iostream>
#include <fstream>

using namespace std;

int depth = 0;
int horizontal = 0;
int aim = 0;

void up(int a) { aim -= a; }
void down(int a) { aim += a; }
void forward(int a) {
  horizontal += a;
  depth += (a * aim);
}

void interpretStatement(string instruction, int number) {
  if (instruction == "up") up(number);
  else if (instruction == "down") down(number);
  else if (instruction == "forward") forward(number);
  else cout << "WARN: Skipping " << instruction << "::" << number << endl;
}

int main() {
  ifstream inFile ("../input");

  string instruction;
  int number;
  while (inFile >> instruction >> number) {
    interpretStatement(instruction, number);
  }
  
  cout << depth*horizontal << endl;
}
