import os
import json
import csv
import datetime as dt
import timedelta as td

csvDataPath = "csv"
resultPath = "result"


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "is been created.")


extractedDataList = []
extractedPowerList = []
# Extract data
fileList = os.listdir(csvDataPath)
fileList.sort()
for fileName in fileList:
    file = open(csvDataPath + "/" + fileName)
    currentCsvFile = csv.reader(file)

    if "sensor" in fileName:
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

    else:
        timeIndex = 0
        topicIndex = 0
        messageIndex = 0
        indexLine = True
        for line in currentCsvFile:
            # Find index positions
            if indexLine:
                count = 0
                for element in line:
                    if 'time' == element:
                        timeIndex = count
                    elif 'topic' == element:
                        topicIndex = count
                    elif 'message' == element:
                        messageIndex = count
                    count += 1
                indexLine = False
                continue

            # Fill dictionary
            if "POWER2" in line[topicIndex]:
                try:
                    time = line[timeIndex]
                    power = line[messageIndex]
                    extractedData = {
                        'Time': time,
                        'Power2': power
                    }
                    extractedPowerList.append(extractedData)
                except:
                    continue

    file.close()

# Filter
filteredExtractedData = []
filteredExtractedPower = []
for extractedData in extractedPowerList:
    timeString = extractedData["Time"][1:-1]
    time = str.split(timeString, ", ")
    dateTime = dt.datetime(int(time[0]), int(time[1]), int(time[2]),
                           int(time[3]), int(time[4]), int(time[5]))
    extractedData["Time"] = dateTime
    # Test Period
    if dateTime > dt.datetime(2022, 11, 16, 9, 5) and dateTime < dt.datetime(2022, 11, 30, 12, 16):
        if dateTime.time() < dt.time(7, 30) or dateTime.time() > dt.time(16, 30):
            filteredExtractedPower.append(extractedData)

for extractedData in extractedDataList:
    dateTime = dt.datetime.strptime(extractedData["Time"], '%Y-%m-%dT%H:%M:%S')
    # Test Period
    if dateTime > dt.datetime(2022, 11, 16, 9, 5) and dateTime < dt.datetime(2022, 11, 30, 12, 16):
        if dateTime.time() < dt.time(7, 30) or dateTime.time() > dt.time(16, 30):
            motion = False
            for power in extractedPowerList:
                if dateTime < power["Time"] and dateTime + dt.timedelta(minutes=5) > power["Time"]:
                    motion = True
                    break

            extractedData["Light"] = extractedData["Illuminance"] > 10
            extractedData["Motion"] = motion
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
