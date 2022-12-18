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
extractedPowerList = []
# Extract data
fileList = os.listdir(csvDataPath)
fileList.sort()
for fileName in fileList:
    file = open(csvDataPath + "/" + fileName)
    currentCsvFile = csv.reader(file)

    if "sensor" in fileName:
        timeIndex = 0
        illuminanceIndex = 0
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
            if "POWER1" in line[topicIndex]:
                try:
                    time = line[timeIndex]
                    power = line[messageIndex]
                    extractedData = {
                        'Time': time,
                        'Power1': power
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
    if dateTime > dt.datetime(2022, 12, 1, 11, 15) and dateTime < dt.datetime(2022, 12, 8, 11, 20):
        if dateTime.time() < dt.time(7, 30) or dateTime.time() > dt.time(16, 30):
            filteredExtractedPower.append(extractedData)

for extractedData in extractedDataList:
    dateTime = dt.datetime.strptime(extractedData["Time"], '%Y-%m-%dT%H:%M:%S')
    # Test Period
    if dateTime > dt.datetime(2022, 12, 1, 11, 15) and dateTime < dt.datetime(2022, 12, 8, 11, 20):
        if dateTime.time() < dt.time(7, 30) or dateTime.time() > dt.time(16, 30):
            motion = False
            for power in extractedPowerList:
                if dateTime < power["Time"] and dateTime + dt.timedelta(minutes=5) > power["Time"]:
                    motion = True
                    break

            extractedData["Light"] = extractedData["Illuminance"] > 8
            extractedData["Motion"] = motion
            filteredExtractedData.append(extractedData)

# Save data
createPath(resultPath)
csvFile = open(resultPath + "/dining-room.csv", "w")
writer = csv.writer(csvFile)

indexLine = True
for extractedData in filteredExtractedData:
    if indexLine:
        writer.writerow(extractedData.keys())
        indexLine = False
    writer.writerow(extractedData.values())

csvFile.close()

# Create final results

# Result
csvFile = open(resultPath + "/dining-room-results.csv", "w")
writer = csv.writer(csvFile)

light = 0
motion = 0
lightAndMotion = 0
lightAndNotMotion = 0
notLightAndMotion = 0
for extractedData in filteredExtractedData:
    lightVal = extractedData["Light"]
    motionVal = extractedData["Motion"]
    if lightVal:
        light += 1
        if not motionVal:
            lightAndNotMotion += 1
    if motionVal:
        motion += 1
        if not lightVal:
            notLightAndMotion += 1
    if lightVal and motionVal:
        lightAndMotion += 1

results = {
    'Licht-Perioden': light,
    'Anwesenheits-Perioden': motion,
    'Ausgewertete Perioden': len(filteredExtractedData),
    'Licht mit Anwesenheit der Nutzer': lightAndMotion,
    'Licht ohne Anwesenheit der Nutzer': lightAndNotMotion,
    'Kein Licht mit Anwesenheit der Nutzer': notLightAndMotion
}

writer.writerow(results.keys())
writer.writerow(results.values())

csvFile.close()

# Result per day
csvFile = open(resultPath + "/dining-room-results-per-day.csv", "w")
writer = csv.writer(csvFile)

lastDateTime = dt.datetime.now() - dt.timedelta(365)
resultPerDay = []

elementCounter = 0
light = 0
motion = 0
lightAndMotion = 0
lightAndNotMotion = 0
notLightAndMotion = 0

for extractedData in filteredExtractedData:
    currentDateTime = dt.datetime.strptime(
        extractedData["Time"], '%Y-%m-%dT%H:%M:%S')
    if currentDateTime.date() != lastDateTime.date():
        if elementCounter != 0:
            result = {
                'Datum': lastDateTime.strftime('%Y-%m-%d'),
                'Licht-Perioden': light,
                'Anwesenheits-Perioden': motion,
                'Ausgewertete Perioden': elementCounter,
                'Licht mit Anwesenheit der Nutzer': lightAndMotion,
                'Licht ohne Anwesenheit der Nutzer': lightAndNotMotion,
                'Kein Licht mit Anwesenheit der Nutzer': notLightAndMotion
            }
            resultPerDay.append(result)
        lastDateTime = currentDateTime
        elementCounter = 0
        light = 0
        motion = 0
        lightAndMotion = 0
        lightAndNotMotion = 0
        notLightAndMotion = 0
    lightVal = extractedData["Light"]
    motionVal = extractedData["Motion"]
    if lightVal:
        light += 1
        if not motionVal:
            lightAndNotMotion += 1
    if motionVal:
        motion += 1
        if not lightVal:
            notLightAndMotion += 1
    if lightVal and motionVal:
        lightAndMotion += 1
    elementCounter += 1

if elementCounter != 0:
    result = {
        'Datum': lastDateTime.strftime('%Y-%m-%d'),
        'Licht-Perioden': light,
        'Anwesenheits-Perioden': motion,
        'Ausgewertete Perioden': elementCounter,
        'Licht mit Anwesenheit der Nutzer': lightAndMotion,
        'Licht ohne Anwesenheit der Nutzer': lightAndNotMotion,
        'Kein Licht mit Anwesenheit der Nutzer': notLightAndMotion
    }
    resultPerDay.append(result)

if len(resultPerDay) > 0:
    writer.writerow(resultPerDay[0].keys())
    for result in resultPerDay:
        writer.writerow(result.values())

csvFile.close()
