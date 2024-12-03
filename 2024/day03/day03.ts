// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const input = (await Bun.file("input").text()).trim().replaceAll(EOL, " ");

let allMulInstructions = 0;
let activeMulInstructions = 0;

let ctx: string = "";
let conditionalsEnabled = true;
for (let char of input) {
    ctx += char;
    if (ctx.endsWith("do()")) {
        conditionalsEnabled = true;
        ctx = "";
    } else if (ctx.endsWith("don't()")) {
        conditionalsEnabled = false;
        ctx = "";
    } else {
        const mulInstruction = ctx.match(/mul\((\d{1,3}),(\d{1,3})\)$/);
        if (!mulInstruction) continue;

        const result = parseInt(mulInstruction[1]) * parseInt(mulInstruction[2]);
        allMulInstructions += result;
        if (conditionalsEnabled) {
            activeMulInstructions += result;
        }
    }
}

console.log("Part 1:", allMulInstructions);
console.log("Part 2:", activeMulInstructions);
