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
    if "sensor" in fileName:
        file = open(csvDataPath + "/" + fileName)
        currentCsvFile = csv.reader(file)

        timeIndex = 0
        illuminanceIndex = -1
        indexLine = True
        for line in currentCsvFile:
            # Find index positions
            if indexLine:
                count = 0
                for element in line:
                    if 'Time' == element:
                        timeIndex = count
                    elif 'BH1750' == element:
                        illuminanceIndex = count
                    count += 1
                indexLine = False
                continue

            # Fill dictionary
            try:
                time = line[timeIndex]
                bh1750 = line[illuminanceIndex].replace("'", '"')
                illuJson = json.loads(bh1750)
                extractedData = {
                    'Time': time,
                    'Illuminance': illuJson["Illuminance"]
                }
                extractedDataList.append(extractedData)
            except:
                continue

        file.close()

# Filter
filteredExtractedData = []
for extractedData in extractedDataList:
    dateTime = dt.datetime.strptime(extractedData["Time"], '%Y-%m-%dT%H:%M:%S')
    # Test Period
    if dateTime > dt.datetime(2022, 11, 16, 9, 5) and dateTime < dt.datetime(2022, 11, 30, 12, 16):
        if dateTime.time() < dt.time(7, 30) or dateTime.time() > dt.time(16, 30):
            filteredExtractedData.append(extractedData)

# Save data
createPath(resultPath)
csvFile = open(resultPath + "/living-room.csv", "w")
writer = csv.writer(csvFile)

indexLine = True
for extractedData in filteredExtractedData:
    if indexLine:
        writer.writerow(extractedData.keys())
        indexLine = False
    writer.writerow(extractedData.values())

csvFile.close()
