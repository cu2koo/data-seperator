import os
import json
import csv
import datetime as dt

csvDataPath = "csv"
resultPath = "result"

# Time Period (08.12.2022 11:20 - 15.12.2022 04:00)
periodBegin = dt.datetime(2022, 12, 8, 11, 20)
periodEnd = dt.datetime(2022, 12, 15, 4, 0)

# Result file name
resultFileName = "bath"


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "is been created.")


def extractAm2301Data(files):
    extractedDataList = []
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
                        'Date': time,
                        'Temperature': tempJson["Temperature"],
                        'Humidity': tempJson["Humidity"],
                        'Dew Point': tempJson["DewPoint"],
                        'Unit': unit
                    }
                    extractedDataList.append(extractedData)
                except:
                    continue

    return extractedDataList


def filterAm2301Data(extractedDataList, timePeriodBegin, timePeriodEnd):
    filteredExtractedData = []
    for extractedData in extractedDataList:
        dateTime = dt.datetime.strptime(
            extractedData["Date"], '%Y-%m-%dT%H:%M:%S')
        # Test Period
        if dateTime > timePeriodBegin and dateTime < timePeriodEnd:
            filteredExtractedData.append(extractedData)

    return filteredExtractedData


def saveResult(writer, filteredExtractedData):
    indexLine = True
    for extractedData in filteredExtractedData:
        if indexLine:
            writer.writerow(extractedData.keys())
            indexLine = False
        writer.writerow(extractedData.values())


# Extract data
fileList = os.listdir(csvDataPath)
fileList.sort()
extractedDataList = extractAm2301Data(fileList)

# Filter
filteredExtractedData = filterAm2301Data(
    extractedDataList, periodBegin, periodEnd)

# Save data
createPath(resultPath)
csvFile = open(resultPath + "/" + resultFileName +
               ".csv", "w", encoding="utf-8", newline='')
writer = csv.writer(csvFile)
saveResult(writer, filteredExtractedData)
csvFile.close()

# Extra measurements
periodBegin = dt.datetime(2022, 12, 16, 0, 0)
periodEnd = dt.datetime(2022, 12, 19, 0, 0)

# Filter
filteredExtractedData = filterAm2301Data(
    extractedDataList, periodBegin, periodEnd)

csvFile = open(resultPath + "/" + resultFileName +
               "-extra.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(csvFile)
saveResult(writer, filteredExtractedData)
csvFile.close()
