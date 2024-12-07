// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const inputLines = (await Bun.file("input").text()).trim().split(EOL);

type Equation = { total: number, values: Array<number> };
const OPERATORS = ["+", "*"] as const;
type Operator = (typeof OPERATORS)[number];

function testSolution(equation: Equation, operators: Array<Operator>) {
    let computedSolution = equation.values[0];
    for (let inx = 0; inx < equation.values.length; inx++) {
        const value = equation.values[inx + 1];
        switch (operators[inx]) {
            case "+": computedSolution += value; break;
            case "*": computedSolution *= value; break;
        }
    }
    return computedSolution === equation.total;
}

function generateCandidates(equation: Equation, prev: Array<Operator>): Array<Array<Operator>> {
    if (prev.length == (equation.values.length - 1)) return [prev];
    const candidates: Array<Array<Operator>> = [];
    for (let operator of OPERATORS) {
        const extension = [...prev, operator];
        const newCandidates = generateCandidates(equation, extension);
        candidates.push(...newCandidates);
    }
    return candidates;
}

function isPossibleEquation(equation: Equation): boolean {
    const operatorCandidates: Array<Array<Operator>> = generateCandidates(equation, []);

    for (let operatorCandidate of operatorCandidates) {
        if (testSolution(equation, operatorCandidate)) return true;
    }
    
    return false;
}

const equations: Array<Equation> = inputLines.map((line: string) => {
    const [totalString, valuesString] = line.split(/:\s+/);
    const total = parseInt(totalString);
    const values = valuesString.split(/\s+/).map((valueString) => parseInt(valueString));

    return { total, values } as Equation;
});

const solution1 = equations
    .filter(isPossibleEquation)
    .map((equation) => equation.total)
    .reduce((acc, total) => acc + total, 0);

const solution2 = -1;

console.log("Part 1:", solution1);
console.log("Part 2:", solution2);
