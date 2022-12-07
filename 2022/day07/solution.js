const { readFileSync } = require("fs");
const { join: path } = require("path");

class FSNode {
    type = "raw"
    name = null
    size = null
    parent = null

    constructor(name) {
        this.name = name
    }

    getSize = () => this.size

    setParent = (parentNode) => {
        this.parent = parentNode
    }

    static fromDataLine = (dataLine) => {
        const data = dataLine.split(" ");
        if (data[0] == "dir") {
            return new Directory(data[1], []);
        } else {
            return new File(dataLine)
        }
    }
}

class Directory extends FSNode {
    type = "dir"
    children = null

    constructor(name, children = []) {
        super(name);
        this.children = children;
    }

    getSize = () => {
        let total = 0;
        this.children.forEach((child) => {
            total += child.getSize();
        });
        return total;
    }

    addChild = (childNode) => {
        childNode.setParent(this);
        this.children.push(childNode);
    }

    getChild = (childName) => {
        const child = this.children.find((child) => {
            return child.name === childName;
        });
        if (!child)
            throw new Error(`${this.name} doesn't contain ${childName}!`);
        else return child;
    }
}

class File extends FSNode {
    type = "file";

    constructor(name, size=undefined) {
        if (size) {
            super(name);
            this.size = size;
        } else {
            // Allow for passing the input line directly
            const data = name.split(" ");
            super(data[1]);
            this.size = parseInt(data[0])
        }
    }
}

class Shell {
    workingDir = null;

    constructor(startingDir) {
        this.workingDir = startingDir
    }

    eval = (line, getNextLine) => {
        if (!line.startsWith("$"))
            throw new Error("Shell#eval received invalid command (missing $)");

        const words = line.split(" ");
        words.shift(); // Remove leading $
        const cmd = words.shift();
        // `words` now contains the arguments

        if (cmd === "cd") {
            const target = words.shift();
            if (target === "..") this.workingDir = this.workingDir.parent;
            else if (target === "/") {
                while (this.workingDir.name !== "/") {
                    this.eval("$ cd ..");
                }
            } else {
                this.workingDir = this.workingDir.getChild(target);
            }
        } else if (cmd === "ls") {
            let nextLineOffset = 1;
            while (true) {
                const nextLine = getNextLine(nextLineOffset);

                // Stop if the next line doesn't exist or is a new command
                if (!nextLine) break;
                if (nextLine.startsWith("$")) break;

                const newNode = FSNode.fromDataLine(nextLine);
                this.workingDir.addChild(newNode);
                nextLineOffset += 1;
            }
        } else 
            throw new Error(`Shell#eval received invalid command (${cmd})`);
    }
}

const rootNode = new Directory("/");
const shell = new Shell(rootNode);

const input = readFileSync(path(__dirname, "input")).toString();
const inputLines = input.split("\n")
for (let _inputLineInx in inputLines) {
    inputLineInx = parseInt(_inputLineInx)
    const inputLine = inputLines[inputLineInx]
    if (inputLine.startsWith("$")) {
        shell.eval(inputLine, (offset=1) => {
            return inputLines[inputLineInx + offset];
        });
    }
}

const getAllDirs = (root) => {
    let result = [root];
    const subDirs = root.children.filter((child) => child.type === "dir");
    subDirs.forEach((subDir) => { result = [...result, ...getAllDirs(subDir)] });
    return result;
};

const allSizes = getAllDirs(rootNode).map((dir) => dir.getSize());

// PART 1: Combine the sizes of all dirs below 100K in size
const solution1 = allSizes.reduce((accumulated, nextSolutionSize) => {
    if (nextSolutionSize > 100000) return accumulated;
    else return accumulated + nextSolutionSize;
}, 0);


// PART 2: Find the size of the smallest dir that is at least 30M in size
const fsSize = 70 * 1000000
const updateSize = 30 * 1000000;

const usedSpace = rootNode.getSize();
const freeSpace = fsSize - usedSpace;
const neededSpace = updateSize - freeSpace;

const solution2Candidates = allSizes.filter((size) => size >= neededSpace);
let solution2 = solution2Candidates[0];
solution2Candidates.forEach((candidate) => {
    if (candidate < solution2) { solution2 = candidate; }
});

console.log(solution1);
console.log(solution2);