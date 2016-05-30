from ij import IJ

from os import listdir
import csv

baseDir = "/Volumes/jayaramanlab/Hannah/Experiments/OptogeneticsFreeWalkingArena/1_Data/rewardNeuronScreen_round2/blueBackLight-level3/"
expDir = "5xCsChr/5xCsChr_x_Empty-Gal4_female/"

# pull out all files in experiment directory
filesToAnalyse = []
expDirContent = listdir(baseDir + expDir)

# loop over all ufmf movies
for file in expDirContent:
    if file.endswith(".ufmf"):
        print(file)

        fileName = file
        fileName = "5xCsChr_x_Empty-Gal4_female_repeat2_cam_0_date_2015_07_29_time_21_22_10_v001";

		#IJ.run("Import UFMF", "choose=" + baseDir + expDir + fileName + ".ufmf")
		#IJ.makeRectangle(125, 0, 47, 40); #marks left upper indicator LED

		#IJ.selectWindow(fileName + ".ufmf");
		#IJ.run("Plot Z-axis Profile");

		#IJ.saveAs("Results", baseDir + expDir + fileName + "_luLEDTrace.csv");

		#IJ.selectWindow("Results");
		#IJ.run("Close");

		#IJ.selectWindow(fileName + ".ufmf");
		#IJ.run("Close");

		#IJ.run("Close");


# loop over newly created frame files movies
#for file in expDirContent:
#    if file.endswith("_luLEDTrace.csv"):
#        print(file)
#        filesToAnalyse.append(file)   
        
#numFiles = len(filesToAnalyse)

#for currFile in range(numFiles):
#    maxValue = []
#    fileToAnalyse = csv.reader(open(baseDir + expDir + filesToAnalyse[currFile],'r'))
#    for line in fileToAnalyse:
#        maxValue.append(line[-1])
    
#    maxValue = asarray(maxValue[1:-1]).astype('float')

#    stimOn = where(maxValue>mean(maxValue))

    
#    fileNameParts = filesToAnalyse[currFile].split('_')
#    fileName = '_'.join(fileNameParts[0:-1])

#    print(fileName)
#    print(stimOn[0][0])
    
#    with open(baseDir + expDir + 'fristFrames.csv', 'a') as csvfile:
#        mywriter = csv.writer(csvfile, delimiter=',')
#        mywriter.writerow([fileName] + [stimOn[0][0]])
