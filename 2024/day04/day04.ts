// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const inputLines = (await Bun.file("input").text()).trim().split(EOL);

type Grid = Array<Array<string>>;
type Vector = [number, number]; // [x, y]

const STRAIGHT_DIRECTIONS: Array<Vector> = [[-1, 0], [1, 0], [0, -1], [0, 1]]
const DIAGONAL_DIRECTIONS: Array<Vector> = [[-1, -1], [1, -1], [-1, 1], [1, 1]]

function VALID_DIRECTIONS(part2: boolean): Array<Vector> {
    return part2 ? DIAGONAL_DIRECTIONS : STRAIGHT_DIRECTIONS.concat(DIAGONAL_DIRECTIONS);
}

function vecAdd(one: Vector, two: Vector): Vector {
    return [one[0] + two[0], one[1] + two[1]];
}

function vecNeg(vec: Vector): Vector {
    return [vec[0] * -1, vec[1] * -1];
}

function getFromGrid(point: Vector, grid: Grid): String {
    return grid[point[1]][point[0]];
}

function isInBounds(point: Vector, grid: Grid) {
    return (
        point[1] >= 0 && point[1] < grid.length
        && point[0] >= 0 && point[0] < grid[0].length
    )
}

function locateHints(grid: Grid, hintSymbol: String): Array<Vector> {
    const hints: Array<Vector> = [];
    for (let y: number = 0; y < grid.length; y++) {
        const line = grid[y];
        for (let x: number = 0; x < line.length; x++) {
            if (line[x] == hintSymbol) hints.push([x, y]);
        }
    }
    return hints;
}

function investigateHint(hint: Vector, searchString: String, part2: boolean = false): number {
    let hitCount: number = 0;
    for (let searchDirection of VALID_DIRECTIONS(part2)) {
        const directionString: Array<String> = [];

        let searchLocation = part2 ? vecAdd(hint, vecNeg(searchDirection)) : hint;
        let searchStringIndex = 0;
        while (
            isInBounds(searchLocation, inputGrid)
            && searchStringIndex < searchString.length
        ) {
            // TODO: Maybe fail the direction on first wrong letter?
            
            directionString.push(getFromGrid(searchLocation, inputGrid));
            searchLocation = vecAdd(searchLocation, searchDirection);
            searchStringIndex += 1;
        }
        if (directionString.join("") == searchString) hitCount += 1;
    }
    if (part2) return Number(hitCount == 2);
    else return hitCount;
}

const inputGrid: Grid = inputLines.map((inputLine: string) => inputLine.split(""));

function part1() {
    const hints: Array<Vector> = locateHints(inputGrid, "X");
    const hitCounts: Array<number>= hints.map((hint) => investigateHint(hint, "XMAS"));
    return hitCounts.reduce((acc, hitCount) => acc + hitCount);
}

function part2() {
    const hints: Array<Vector> = locateHints(inputGrid, "A");
    const hitCounts: Array<number> = hints.map((hint) => investigateHint(hint, "MAS", true));
    return hitCounts.reduce((acc, hitCount) => acc + hitCount);
}

console.log("Part 1:", part1());
console.log("Part 2:", part2());
