from queue import PriorityQueue


def readInputFile(path):
    data = {}
    with open(path, "r") as inputFile:
        data["N"] = int(inputFile.readline())
        tmpNextLine = inputFile.readline()
        data["sourceIndex"] = int(tmpNextLine[0])
        data["destinationIndex"] = int(tmpNextLine[2])
        data["searchStrategy"] = int(tmpNextLine[4])
        data["matrix"] = [
            [int(i) for i in inputFile.readline().split()] for _ in range(data["N"])
        ]
        data["heuristicValues"] = [int(i) for i in inputFile.readline().split()]
    return data


def writeOutputFile(path, output):
    with open(path, "w") as outputFile:
        outputFile.write(" ".join([str(i) for i in output["expandedNodes"]]) + "\n")
        if type(output["path"]) == type(""):
            outputFile.write(output["path"])
        else:
            outputFile.write(" ".join([str(i) for i in output["path"]]))
    return True


def getPath(parentsOfNodes, destinationIndex):
    if destinationIndex == 0:
        return [0]
    path = [destinationIndex]
    currentParents = parentsOfNodes[destinationIndex]
    path.append(currentParents[-1])
    while currentParents:
        currentParents = parentsOfNodes[path[-1]]
        if currentParents:
            path.append(currentParents[-1])
    path.reverse()
    return path


def getTotalWeight(parentsOfNodes, destinationIndex):
    path = [destinationIndex]
    currentParents = parentsOfNodes[destinationIndex]
    path.append(currentParents[-1])
    while currentParents:
        currentParents = parentsOfNodes[path[-1]]
        if currentParents:
            path.append(currentParents[-1])
    path.reverse()
    return path


def BFS(data):
    queue = [data["sourceIndex"]]
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    while len(queue) > 0:
        currentNode = queue.pop(0)
        expandedNodes.append(currentNode)
        for node, weight in enumerate(data["matrix"][currentNode]):
            if weight != 0 and node not in queue and node not in expandedNodes:
                if node == data["destinationIndex"]:
                    parentsOfNodes[node].append(currentNode)
                    output = {
                        "queue": queue,
                        "expandedNodes": expandedNodes,
                        "parentsOfNodes": parentsOfNodes,
                        "path": getPath(parentsOfNodes, data["destinationIndex"]),
                    }
                    return output
                queue.append(node)
                parentsOfNodes[node].append(currentNode)

    output = {
        "queue": queue,
        "expandedNodes": expandedNodes,
        "parentsOfNodes": parentsOfNodes,
        "path": "No path",
    }
    return output


def DFS(data):
    stack = [data["sourceIndex"]]
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    tempReverseList = []
    while len(stack) > 0:
        currentNode = stack.pop(-1)
        expandedNodes.append(currentNode)
        if currentNode == data["destinationIndex"]:
            output = {
                "stack": stack,
                "expandedNodes": expandedNodes,
                "parentsOfNodes": parentsOfNodes,
                "path": getPath(parentsOfNodes, data["destinationIndex"]),
            }
            return output
        for node, weight in enumerate(data["matrix"][currentNode]):
            if weight != 0 and node not in expandedNodes:
                tempReverseList.append(node)
                parentsOfNodes[node].append(currentNode)

        stack = stack + list(reversed(tempReverseList))
        tempReverseList = []

    output = {
        "stack": stack,
        "expandedNodes": expandedNodes,
        "parentsOfNodes": parentsOfNodes,
        "path": "No path",
    }
    return output


def UCS(data):
    priorityQueue = PriorityQueue()
    priorityQueue.put((0, data["sourceIndex"]))
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    while not priorityQueue.empty():
        currentNode = priorityQueue.get()
        expandedNodes.append(currentNode[1])
        if currentNode[1] == data["destinationIndex"]:
            output = {
                "priorityQueue": priorityQueue.queue,
                "expandedNodes": expandedNodes,
                "parentsOfNodes": parentsOfNodes,
                "path": getPath(parentsOfNodes, data["destinationIndex"]),
            }
            return output
        for node, weight in enumerate(data["matrix"][currentNode[1]]):
            if weight != 0 and node not in expandedNodes:

                tempNode = (weight + currentNode[0], node)
                isNodeFound = False
                for x in priorityQueue.queue:
                    if tempNode[1] == x[1]:
                        if tempNode[0] < x[0]:
                            priorityQueue.queue.remove(x)
                            priorityQueue.put(tempNode)
                            parentsOfNodes[node] = [currentNode[1]]
                        isNodeFound = True
                        break

                if not isNodeFound:
                    priorityQueue.put(tempNode)
                    parentsOfNodes[node].append(currentNode[1])
                isNodeFound = False

    output = {
        "priorityQueue": priorityQueue.queue,
        "expandedNodes": expandedNodes,
        "parentsOfNodes": parentsOfNodes,
        "path": "No path",
    }
    return output


def IDS(data):
    maxDepth = data["N"] - 1
    currentDepth = 0

    stack = [data["sourceIndex"]]
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    depthOfNodes = {}
    for i in range(data["N"]):
        depthOfNodes[i] = -1

    tempReverseList = []
    while currentDepth <= maxDepth:
        stack = [data["sourceIndex"]]
        expandedNodes = []

        parentsOfNodes = {}
        for i in range(data["N"]):
            parentsOfNodes[i] = []

        depthOfNodes = {}
        for i in range(data["N"]):
            depthOfNodes[i] = -1
        while len(stack) > 0:
            currentNode = stack.pop(-1)
            expandedNodes.append(currentNode)
            if len(expandedNodes) == 1:
                depthOfNodes[currentNode] = 0
            else:
                depthOfNodes[currentNode] = (
                    depthOfNodes[parentsOfNodes[currentNode][0]] + 1
                )
            if currentNode == data["destinationIndex"]:
                output = {
                    "stack": stack,
                    "expandedNodes": expandedNodes,
                    "parentsOfNodes": parentsOfNodes,
                    "path": getPath(parentsOfNodes, data["destinationIndex"]),
                    "depthOfNodes": depthOfNodes,
                }
                return output
            if depthOfNodes[currentNode] >= currentDepth:
                if len(stack) > 0:
                    if depthOfNodes[parentsOfNodes[stack[-1]][0]] + 1 <= maxDepth:
                        continue
                else:
                    break
            for node, weight in enumerate(data["matrix"][currentNode]):
                if weight != 0 and node not in expandedNodes and node not in stack:
                    tempReverseList.append(node)
                    parentsOfNodes[node].append(currentNode)

            stack = stack + list(reversed(tempReverseList))
            tempReverseList = []
        currentDepth += 1

    output = {
        "stack": stack,
        "expandedNodes": expandedNodes,
        "parentsOfNodes": parentsOfNodes,
        "path": "No path",
        "depthOfNodes": depthOfNodes,
    }
    return output


def GBFS(data):
    priorityQueue = PriorityQueue()
    priorityQueue.put(
        (data["heuristicValues"][data["sourceIndex"]], data["sourceIndex"])
    )
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    while not priorityQueue.empty():
        currentNode = priorityQueue.get()
        expandedNodes.append(currentNode[1])
        for node, weight in enumerate(data["matrix"][currentNode[1]]):
            if (
                weight != 0
                and node not in expandedNodes
                and not [item for item in priorityQueue.queue if item[1] == node]
            ):
                if node == data["destinationIndex"]:
                    parentsOfNodes[node].append(currentNode[1])
                    output = {
                        "priorityQueue": priorityQueue.queue,
                        "expandedNodes": expandedNodes,
                        "parentsOfNodes": parentsOfNodes,
                        "path": getPath(parentsOfNodes, data["destinationIndex"]),
                    }
                    return output
                priorityQueue.put((data["heuristicValues"][node], node))
                parentsOfNodes[node].append(currentNode[1])

    output = {
        "priorityQueue": priorityQueue.queue,
        "expandedNodes": expandedNodes,
        "parentsOfNodes": parentsOfNodes,
        "path": "No path",
    }
    return output


def AStar(data):
    priorityQueue = PriorityQueue()
    priorityQueue.put((0, data["sourceIndex"]))
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    while not priorityQueue.empty():
        currentNode = priorityQueue.get()
        expandedNodes.append(currentNode[1])
        if currentNode[1] == data["destinationIndex"]:
            output = {
                "priorityQueue": priorityQueue.queue,
                "expandedNodes": expandedNodes,
                "parentsOfNodes": parentsOfNodes,
                "path": getPath(parentsOfNodes, data["destinationIndex"]),
            }
            return output
        for node, weight in enumerate(data["matrix"][currentNode[1]]):
            if weight != 0 and node not in expandedNodes:
                tempNode = (
                    weight
                    + currentNode[0]
                    + data["heuristicValues"][node]
                    - data["heuristicValues"][currentNode[1]],
                    node,
                )
                isNodeFound = False
                for x in priorityQueue.queue:
                    if tempNode[1] == x[1]:
                        if tempNode[0] < x[0]:
                            priorityQueue.queue.remove(x)
                            priorityQueue.put(tempNode)
                            parentsOfNodes[node] = [currentNode[1]]
                        isNodeFound = True
                        break

                if not isNodeFound:
                    priorityQueue.put(tempNode)
                    parentsOfNodes[node].append(currentNode[1])
                isNodeFound = False

    output = {
        "priorityQueue": priorityQueue.queue,
        "expandedNodes": expandedNodes,
        "parentsOfNodes": parentsOfNodes,
        "path": "No path",
    }
    return output


def main():
    data = readInputFile("input.txt")

    chosenSearchStrategy = data["searchStrategy"]
    output = {}
    if chosenSearchStrategy == 0:
        output = BFS(data)
    elif chosenSearchStrategy == 1:
        output = DFS(data)
    elif chosenSearchStrategy == 2:
        output = UCS(data)
    elif chosenSearchStrategy == 3:
        output = IDS(data)
    elif chosenSearchStrategy == 4:
        output = GBFS(data)
    elif chosenSearchStrategy == 5:
        output = AStar(data)

    writeOutputFile("output.txt", output)


main()