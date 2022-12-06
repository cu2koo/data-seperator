import os
import json
import csv

filter = input("enter your filter (case sensitive): ")
print("your filter is", filter)

rawDataFolderName = "rawdata"
resDataFolderName = "filtered"
csvDataFolderName = "csv"

for fileName in os.listdir(rawDataFolderName):
    if "log000" not in fileName:
        continue

    file = open(rawDataFolderName + "/" + fileName, "r", encoding="utf-8")
    lines = file.readlines()
    file.close()

    filteredLines = []
    for line in lines:
        if filter in line:
            filteredLines.append(line)

    if not os.path.exists(resDataFolderName):
        os.makedirs(resDataFolderName)
        print(resDataFolderName, "is been created.")

    newFile = open(resDataFolderName + "/" + fileName, "w", encoding="utf-8")
    newFile.writelines(filteredLines)
    newFile.close()
    print("----------------------------------------------------------------\n",
          len(filteredLines), "lines found in",
          rawDataFolderName + "/" + fileName + ".\n",
          "result has been saved in", resDataFolderName + "/" + fileName + ".")

    if len(filteredLines) == 0:
        continue

    if not os.path.exists(csvDataFolderName):
        os.makedirs(csvDataFolderName)
        print(csvDataFolderName, "is been created.")

    csvFile = open(csvDataFolderName + "/" + fileName + ".csv", "w")
    csvWriter = csv.writer(csvFile)

    first = True
    for line in filteredLines:
        data = json.loads(line)
        if first:
            csvWriter.writerow(data.keys())
            first = False
            print(csvDataFolderName + "/" + fileName + ".csv", "created.")
        csvWriter.writerow(data.values())

    csvFile.close()

    csvSensorFile = open(csvDataFolderName + "/" +
                         fileName + "_sensor.csv", "w")
    csvSensorWriter = csv.writer(csvSensorFile)
    csvStateFile = open(csvDataFolderName + "/" + fileName + "_state.csv", "w")
    csvStateWriter = csv.writer(csvStateFile)
    csvResultFile = open(csvDataFolderName + "/" +
                         fileName + "_result.csv", "w")
    csvResultWriter = csv.writer(csvResultFile)

    firstSensor = True
    firstState = True
    firstResult = True
    for line in filteredLines:
        data = json.loads(line)
        if "SENSOR" in data["topic"]:
            if firstSensor:
                csvSensorWriter.writerow(data["message"].keys())
                firstSensor = False
                print(csvDataFolderName + "/" +
                      fileName + "_sensor.csv", "created.")
            csvSensorWriter.writerow(data["message"].values())
        if "STATE" in data["topic"]:
            if firstState:
                csvStateWriter.writerow(data["message"].keys())
                firstState = False
                print(csvDataFolderName + "/" +
                      fileName + "_state.csv", "created.")
            csvStateWriter.writerow(data["message"].values())
        if "RESULT" in data["topic"]:
            if firstResult:
                csvResultWriter.writerow(data["message"].keys())
                firstResult = False
                print(csvDataFolderName + "/" +
                      fileName + "_result.csv", "created.")
            csvResultWriter.writerow(data["message"].values())

    csvSensorFile.close()
    csvStateFile.close()
    csvResultFile.close()
