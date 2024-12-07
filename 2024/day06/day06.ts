// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const inputLines = (await Bun.file("input").text()).trim().split(EOL);

const OBSTACLE_MARKER = "#";

class Vector {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    add(other: Vector): Vector { return new Vector(this.x + other.x, this.y + other.y); }
    neg(): Vector { return new Vector(this.x * -1, this.y * -1); }
    eq(other: Vector) { return other.x == this.x && other.y == this.y; }
    toString() { return `(${this.x}|${this.y})`; }
    cpy() { return new Vector(this.x, this.y); }
}
const OUT_OF_BOUNDS: Vector = new Vector(-1, -1);
const GUARD_LOCATION_MAP = {
    "v": new Vector(0, 1),
    "^": new Vector(0, -1),
    "<": new Vector(-1, 0),
    ">": new Vector(1, 0)
};
const DIRECTION_ORDER = [
    GUARD_LOCATION_MAP["^"], GUARD_LOCATION_MAP[">"],
    GUARD_LOCATION_MAP["v"], GUARD_LOCATION_MAP["<"],
    GUARD_LOCATION_MAP["^"]
]

type Grid = Array<Array<string>>;
class Laboratory {
    height: number;
    width: number;

    obstacles: VectorList;
    guard: Guard;

    constructor(input: Grid) {
        this.height = input.length;
        this.width = input[0].length;

        this.obstacles = new VectorList();
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const char = input[y][x];
                if (char == OBSTACLE_MARKER) this.obstacles.push(new Vector(x, y));
                else if (GUARD_LOCATION_MAP.hasOwnProperty(char)) {
                    this.guard = new Guard([new Vector(x, y), GUARD_LOCATION_MAP[char], this]);
                }
            }
        }
    }
}
type Position = [Vector, Vector, Laboratory];
function cpyPosition(position: Position): Position {
    return [position[0].cpy(), position[1].cpy(), position[2]]
}
class History extends Array<Position> {
    includes(pos: Position) {
        for (let checkPosition of this) {
            if (checkPosition[0].eq(pos[0])) return true;
        }
        return false;
    }
}
class VectorList extends Array<Vector> {
    includes(vec: Vector) {
        for (let vector of this) {
            if (vector.eq(vec)) return true;
        }
        return false;
    }
}

class Guard {
    position: Position;
    history: History = []

    constructor(position: Position) {
        this.position = position;
    }

    facing(): Vector {
        return this.position[0].add(this.position[1]);
    }

    rotateRight() {
        for (let directionInx = 0; directionInx < DIRECTION_ORDER.length; directionInx++) {
            if (this.position[1].eq(DIRECTION_ORDER[directionInx])) {
                this.position[1] = DIRECTION_ORDER[directionInx + 1];
                return;
            }
        }
    }

    tick() {
        const newLocation = this.facing();
        if (this.position[2].obstacles.includes(newLocation)) this.rotateRight();
        else if (
                (newLocation.x >= this.position[2].width)
                || (newLocation.x < 0)
                || (newLocation.y >= this.position[2].height)
                || (newLocation.y < 0)
        ) {
            this.position[0] = OUT_OF_BOUNDS;
            return;
        } else this.position[0] = newLocation;

        if (this.history.includes(this.position)) {
            console.warn(
                "Duplicate guard loc+dir:",
                this.position[0].toString(),
                this.position[1].toString()
            );
        }
        this.history.push(cpyPosition(this.position));
    }

    isInField() { return !this.position[0].eq(OUT_OF_BOUNDS); }
}

const laboratory = new Laboratory(inputLines.map((line: string) => line.split("")));
while (laboratory.guard.isInField()) {
    laboratory.guard.tick();
}

let uniqueSpots: VectorList = new VectorList();
const solution1 = laboratory.guard.history.reduce((acc, historyEntry) => {
    if (!uniqueSpots.includes(historyEntry[0])) {
        uniqueSpots.push(historyEntry[0]);
        acc += 1;
    }
    return acc;
}, 0);

// @ts-ignore
Bun.write(
    // @ts-ignore
    Bun.file("debug"),
    uniqueSpots.map((spot, inx) => (
        spot.toString()
        + ((inx+1) % 10 == 0 ? EOL : " "))
    )
);

console.log("Part 1:", solution1);
