// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const inputLines = (await Bun.file("input").text()).trim().split(EOL);

type Grid = Array<Array<string>>;
type Vector = [number, number]; // [x, y]

const SEARCH_STRING = "MAS";
const VALID_DIRECTIONS: Array<Vector> = [
    [-1, -1], [1, -1], [-1, 1], [1, 1] // Diagonals
];

const HINT_SYMBOL = SEARCH_STRING.split("")[1];

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

function locateHints(grid: Grid): Array<Vector> {
    const hints: Array<Vector> = [];
    for (let y: number = 0; y < grid.length; y++) {
        const line = grid[y];
        for (let x: number = 0; x < line.length; x++) {
            if (line[x] == HINT_SYMBOL) hints.push([x, y]);
        }
    }
    return hints;
}

function investigateHint(hint: Vector): boolean {
    let hitCount: number = 0;
    for (let searchDirection of VALID_DIRECTIONS) {
        const directionString: Array<String> = [];

        let searchLocation = vecAdd(hint, vecNeg(searchDirection));
        let searchStringIndex = 0;
        while (
            isInBounds(searchLocation, inputGrid)
            && searchStringIndex < SEARCH_STRING.length
        ) {
            // TODO: Maybe fail the direction on first wrong letter?
            
            directionString.push(getFromGrid(searchLocation, inputGrid));
            searchLocation = vecAdd(searchLocation, searchDirection);
            searchStringIndex += 1;
        }
        if (directionString.join("") == SEARCH_STRING) hitCount += 1;
    }
    return hitCount == 2;
}

const inputGrid: Grid = inputLines.map((inputLine: string) => inputLine.split(""));
const hints: Array<Vector> = locateHints(inputGrid);
const totalHitCount = hints.map(investigateHint).reduce((acc, didHit) => didHit ? acc + 1 : acc, 0);
console.log("Part 2:", totalHitCount);
