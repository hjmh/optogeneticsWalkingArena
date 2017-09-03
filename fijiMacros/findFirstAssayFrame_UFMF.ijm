baseDir = "/Volumes/jayaramanlab/Hannah/Projects/OptoFreeWalking/1_Data/RewardTest_Laura/fullFieldPulse/"

expDir = "MB001B_x_20xCsChrimsonWTB_male_Wuerzburg/200ms/"
fileName = "MB001B_x_20xCsChrimsonWTB_10LED_0-2s_RetWuerzburg_male_12h_rep3_2017_08_10_12_29_36_v001"

run("Import UFMF", "choose=" + baseDir + expDir + fileName + ".ufmf");
makeRectangle (30, 0, 25, 25);  //marks left upper indicator LED

selectWindow(fileName + ".ufmf");
run("Plot Z-axis Profile");

saveAs("Results", baseDir + expDir + fileName + "_luLEDTrace.csv");

close(fileName + ".ufmf");
close("Results");
close();

//now use python script to extract first frames and write those to file...

