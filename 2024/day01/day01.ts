// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const inputLines = (await Bun.file("input").text()).trim().split(EOL);

let left: Array<number> = [];
let right: Array<number> = [];

class DMap<K> extends Map<K, number> {
    getOrDefault(inx: K, fallback: number) { return this.get(inx) ?? fallback; }
    getOrZero(inx: K) { return this.getOrDefault(inx, 0); }
    increment(inx: K) { this.set(inx, this.getOrZero(inx) + 1); }
}

inputLines
    .map((line: string) => line.trim())
    .forEach((line: string) => {
        const match = line.match(/(\d+)\s+(\d+)/)!;
        left.push(parseInt(match[1]));
        right.push(parseInt(match[2]));
    });
left = left.sort();
right = right.sort();

let solution1 = 0;
let solution2 = 0;

const rightOccurences: DMap<number> = new DMap();
for (const inx in left) {
    const lnum = left[inx];
    const rnum = right[inx];

    solution1 += Math.abs(lnum - rnum);
    rightOccurences.increment(rnum);
}

solution2 = left.reduce((acc, lnum) => acc + (lnum * rightOccurences.getOrZero(lnum)), 0);

console.log(`Part 1: ${solution1}${EOL}Part 2: ${solution2}`);
