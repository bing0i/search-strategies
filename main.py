def readInputFile(path):
    input = {}
    with open(path, "r") as inputFile:
        input["N"] = int(inputFile.readline())
        tmpNextLine = inputFile.readline()
        input["sourceIndex"] = int(tmpNextLine[0])
        input["destinationIndex"] = int(tmpNextLine[2])
        input["searchStrategy"] = int(tmpNextLine[4])
        input["matrix"] = []
        for i in range(input["N"]):
            input["matrix"] = input["matrix"] + inputFile.readline().split()
        input["heuristicValues"] = inputFile.readline().split()
    return input


print(readInputFile("input.txt"))
