// @ts-ignore - tl_ls is missing @types/node
import { EOL } from "node:os";
// @ts-ignore - tl_ls doesn't know about Bun
const inputSections = (await Bun.file("input").text()).trim().split(`${EOL}${EOL}`);

declare global {
    interface Array<T> {
        biFilter(filter: (subj: T) => boolean): [Array<T>, Array<T>];
        getMiddle(): T;
        remove(candidate: T): void;
    }
}

Array.prototype.biFilter = function<T>(this: Array<T>, filter: (subj: T) => boolean) {
    const matches: Array<T> = [];
    const unmatches: Array<T> = [];
    this.forEach((elem: T) => {
        if (filter(elem)) matches.push(elem);
        else unmatches.push(elem);
    });
    return [matches, unmatches];
}
Array.prototype.getMiddle = function<T>(this: Array<T>) {
    if (this.length == 0) return 0; // For skipping unfixable updates in part2

    let middleInx = Math.floor((this.length - 1) / 2);
    if (middleInx % 1 != 0) {
        console.warn("Unclear middle index", middleInx, "for", this, "(rounding down)");
        middleInx = Math.floor(middleInx);
    }
    return this[middleInx];
}
Array.prototype.remove = function<T>(this: Array<T>, candidate: T) {
    let inx = this.indexOf(candidate);
    while (inx != -1) {
        this.splice(inx, 1);
        inx = this.indexOf(candidate);
    }
}

const rules: Array<[number, number]> = inputSections[0]
    .split(EOL)
    .map((ruleLine: string) => (
        ruleLine.split("|").map((pageNumStr) => parseInt(pageNumStr))
    ));
const updates: Array<Array<number>> = inputSections[1]
    .split(EOL)
    .map((updateLine: string) => (
        updateLine.split(",").map((pageNumStr) => parseInt(pageNumStr))
    ));

const dependencyMap: Map<number, Array<number>> = new Map();
for (let [earlier, later] of rules) {
    // Push to potentially existing array, else create new one
    dependencyMap.get(later)?.push(earlier)
    ?? dependencyMap.set(later, [earlier]);
}

function isValidUpdate(update: Array<number>): boolean {
    const banList: Array<number> = [];
    for (let page of update) {
        if (banList.includes(page)) return false;

        const newBans = dependencyMap.get(page);
        if (newBans) banList.push(...newBans);
    }
    return true;
}

function reconstructUpdate(update: Array<number>): Array<number> {
        // Enumerate relevant dependencies
        const missingDependencies: Map<number, Array<number>> = new Map();
        for (const page of update) {
            const pageDependencies = dependencyMap.get(page)
                ?.filter((dependencyPage) => update.includes(dependencyPage))
                ?? [];
            missingDependencies.set(page, pageDependencies);
        }

        // Re-construct the update in a valid order
        const fixedUpdate: Array<number> = [];
        while (missingDependencies.size > 0) {
            let loopc = 0;
            for (let [page, dependencies] of missingDependencies.entries()) {
                if (loopc > missingDependencies.size) {
                    console.warn("Skipping unfixable update:", update);
                    return [];
                }
                if (dependencies.length > 0) continue;

                loopc = 0;
                fixedUpdate.push(page);
                missingDependencies.delete(page);
                for (let [_, otherPageDependencies] of missingDependencies) {
                    otherPageDependencies.remove(page);
                }
            }
        }

        return fixedUpdate;
}


const [validUpdates, invalidUpdates] = updates.biFilter(isValidUpdate);

const solution1 = validUpdates
    .map((validUpdate) => validUpdate.getMiddle())
    .reduce((acc, middleNum) => acc + middleNum);

const solution2 = invalidUpdates
    .map((invalidUpdate) => reconstructUpdate(invalidUpdate).getMiddle())
    .reduce((acc, middleNum) => acc + middleNum);

console.log("Part 1:", solution1);
console.log("Part 2:", solution2);
