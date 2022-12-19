import os
import json
import csv

filter = input("enter your filter (case sensitive): ")
print("your filter is", filter)

rawDataPath = "data"
resDataPath = "filtered"
csvDataPath = "csv"


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "is been created.")


def readFileLines(path, fileName):
    file = open(path + "/" + fileName, "r", encoding="utf-8")
    lines = file.readlines()
    file.close()

    return lines


def writeFileLines(path, fileName, fileLines):
    file = open(path + "/" + fileName, "w", encoding="utf-8", newline='')
    file.writelines(fileLines)
    file.close()
    print(path + "/" + fileName, "is been created with", len(fileLines), "lines.")


def filterFileLines(filter, fileLines):
    filteredFileLines = []
    for line in fileLines:
        if filter in line:
            filteredFileLines.append(line)

    return filteredFileLines


def writeCsvFileLines(path, fileName, fileLines, topic=None):
    csvs = {}
    files = []
    for line in fileLines:
        data = json.loads(line)
        if topic is not None:
            data = data[topic]
        key = listToString(list(data.keys()))
        if key not in csvs.keys():
            number = len(csvs) + 1
            csvFile = open(path + "/" + fileName + "-" +
                           str(number) + ".csv", "w", newline='')
            print(path + "/" + fileName + "-" + str(number) + ".csv",
                  "is been created.")
            files.append(csvFile)
            csvs[key] = csv.writer(csvFile)
            csvs[key].writerow(data.keys())
        csvs[key].writerow(data.values())

    for file in files:
        file.close()


def listToString(list):
    result = ""
    for item in list:
        result += item

    return result


for fileName in os.listdir(rawDataPath):
    if "log000" not in fileName:
        continue

    # Filter data from the rawDataPath via filter
    lines = readFileLines(rawDataPath, fileName)
    filteredLines = filterFileLines(filter, lines)
    createPath(resDataPath)
    writeFileLines(resDataPath, fileName, filteredLines)
    if len(filteredLines) == 0:
        continue

    # Create csv files from resDataPath
    createPath(csvDataPath)
    writeCsvFileLines(csvDataPath, fileName, filteredLines)

    # Create specific csv files form resDataPath
    sensorLines = filterFileLines("SENSOR", filteredLines)
    writeCsvFileLines(csvDataPath, fileName +
                      "_sensor", sensorLines, "message")
    # Optional
    # stateLines = filterFileLines("STATE", filteredLines)
    # writeCsvFileLines(csvDataPath, fileName +
    #                   "_state", stateLines, "message")
