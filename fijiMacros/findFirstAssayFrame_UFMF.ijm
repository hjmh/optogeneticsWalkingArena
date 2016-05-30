baseDir = "/Volumes/jayaramanlab/Hannah/Experiments/OptogeneticsFreeWalkingArena/1_Data/rewardNeuronScreen_round2/blueBackLight-level3/"
expDir = "20xCsChr/20xCsChr_x_HC-Gal4_female/"
fileName = "20xCsChr_x_HC-Gal4_female_repeat3_cam_0_date_2015_08_01_time_21_50_49_v001"

run("Import UFMF", "choose=" + baseDir + expDir + fileName + ".ufmf");
makeRectangle(125, 0, 47, 40); //marks left upper indicator LED

selectWindow(fileName + ".ufmf");
run("Plot Z-axis Profile");

saveAs("Results", baseDir + expDir + fileName + "_luLEDTrace.csv");

close(fileName + ".ufmf");
close("Results");
close();

//now use python script to extract first frames and write those to file...

