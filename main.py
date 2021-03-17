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


# TODO: check against current path to avoid infinite loop
def DFS(data):
    stack = [data["sourceIndex"]]
    expandedNodes = []

    parentsOfNodes = {}
    for i in range(data["N"]):
        parentsOfNodes[i] = []

    while len(stack) > 0:
        currentNode = stack.pop(-1)
        expandedNodes.append(currentNode)
        for node, weight in reversed(list(enumerate(data["matrix"][currentNode]))):
            if weight != 0 and node not in stack and node not in expandedNodes:
                if node == data["destinationIndex"]:
                    parentsOfNodes[node].append(currentNode)
                    output = {
                        "stack": stack,
                        "expandedNodes": expandedNodes,
                        "parentsOfNodes": parentsOfNodes,
                        "path": getPath(parentsOfNodes, data["destinationIndex"]),
                    }
                    return output
                stack.append(node)
                parentsOfNodes[node].append(currentNode)

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
        print(priorityQueue.queue)
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


data = readInputFile("input.txt")
writeOutputFile("output.txt", BFS(data))

print(UCS(data))