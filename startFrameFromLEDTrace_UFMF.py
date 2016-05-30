from os import listdir
import csv
from Tkinter import Tk
from tkFileDialog import askdirectory
from numpy import mean, asarray, where, zeros

root = Tk()
root.withdraw() #prevents root window from appearing
baseDir = askdirectory(initialdir = "/Volumes/jayaramanlab/Hannah/Experiments/OptogeneticsFreeWalkingArena/1_Data/",
                           title = "Select experiment directory (e.g. 5xCsChr)") # "open" dialogue

#baseDir = "/Volumes/jayaramanlab/Hannah/Experiments/OptogeneticsFreeWalkingArena/1_Data/rewardNeuronScreen_round2/blueBackLight-level3/5xCsChr/"
baseDir = baseDir + "/"

fileTrunk = baseDir.split('/')[-2] #every folder to analyse within the base directory should start with this prefix
baseDirContent = listdir(baseDir)

for expDir in baseDirContent:
    print(expDir)

    # expDir to be analysed should have form  "5xCsChr_x_HC-Gal4_female"
    expDir = expDir + "/luLEDTraces/"

    if(fileTrunk not in expDir):
        print(fileTrunk + " not in " + expDir)
        continue

    experiment = expDir.split('/')[0]

    filesToAnalyse = []
    expDirContent = listdir(baseDir + expDir)
    for file in expDirContent:
        if file.endswith('_luLEDTrace.csv'):
            print(file)
            filesToAnalyse.append(file)
    numFiles = len(filesToAnalyse)

    with open(baseDir + expDir + 'firstFrames.csv', 'w') as csvfile:
            mywriter = csv.writer(csvfile, delimiter=',')
            mywriter.writerow(['experiment'] + ['fileName'] + ['startFrame'])

    for currFile in range(numFiles):
        maxValue = []
        fileToAnalyse = csv.reader(open(baseDir + expDir + filesToAnalyse[currFile],'r'))
        for line in fileToAnalyse:
            maxValue.append(line[-1])

        maxValue = asarray(maxValue[1:-1]).astype('float')
        stimOn = where(maxValue>mean(maxValue))

        fileNameParts = filesToAnalyse[currFile].split('_')
        fileName = '_'.join(fileNameParts[0:-1])

        with open(baseDir + expDir + 'firstFrames.csv', 'a') as csvfile:
            mywriter = csv.writer(csvfile, delimiter=',')
            mywriter.writerow([experiment] + [fileName] + [stimOn[0][0]])
