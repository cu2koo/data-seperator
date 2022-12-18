import os
import json
import csv
import datetime as dt

csvDataPath = "csv"
resultPath = "result"


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "is been created.")


extractedDataList = []
# Extract data
fileList = os.listdir(csvDataPath)
fileList.sort()
for fileName in fileList:
    file = open(csvDataPath + "/" + fileName)
    currentCsvFile = csv.reader(file)

    if "sensor" in fileName:
        timeIndex = 0
        tempIndex = 0
        unitIndex = 0
        indexLine = True
        for line in currentCsvFile:
            # Find index positions
            if indexLine:
                count = 0
                for element in line:
                    if 'Time' == element:
                        timeIndex = count
                    elif 'AM2301' == element:
                        tempIndex = count
                    elif 'TempUnit' == element:
                        unitIndex = count
                    count += 1
                indexLine = False
                continue

            # Fill dictionary
            try:
                time = line[timeIndex]
                am2301 = line[tempIndex].replace("'", '"')
                tempJson = json.loads(am2301)
                unit = line[unitIndex]
                extractedData = {
                    'Datum': time,
                    'Temperatur': tempJson["Temperature"],
                    'Luftfeuchtigkeit': tempJson["Humidity"],
                    'Taupunkt': tempJson["DewPoint"],
                    'Einheit': unit
                }
                extractedDataList.append(extractedData)
            except:
                continue

# Filter
filteredExtractedData = []
for extractedData in extractedDataList:
    dateTime = dt.datetime.strptime(
        extractedData["Datum"], '%Y-%m-%dT%H:%M:%S')
    # Test Period
    if dateTime > dt.datetime(2022, 12, 8, 11, 20) and dateTime < dt.datetime(2022, 12, 15, 4, 0):
        filteredExtractedData.append(extractedData)


# Save data
createPath(resultPath)
csvFile = open(resultPath + "/bath.csv", "w")
writer = csv.writer(csvFile)

indexLine = True
for extractedData in filteredExtractedData:
    if indexLine:
        writer.writerow(extractedData.keys())
        indexLine = False
    writer.writerow(extractedData.values())

csvFile.close()

# Reformat data
file = open(resultPath + "/bath.csv", "r")
lines = file.readlines()
file.close()

file = open(resultPath + "/bath-reformated.csv", "w")
for line in lines:
    l = str.replace(line, ",", ";")
    l = str.replace(l, ".", ",")
    file.write(l)
file.close()
