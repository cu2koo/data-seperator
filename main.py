import os

filter = input("enter your filter (case sensitive): ")
print("your filter is", filter)

rawDataFolderName = "rawdata"
resDataFolderName = "filtered"

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
    print(len(filteredLines), "lines found in",
          rawDataFolderName + "/" + fileName + ".",
          "result has been saved in", resDataFolderName + "/" + fileName + ".")
