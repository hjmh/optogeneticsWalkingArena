// Run this to extract a small set of frames 
// ("key frames": frame near end of each stimulation block)

// baseDir = "/Volumes/jayaramanlab/Hannah/Experiments/OptogeneticsFreeWalkingArena/1_Data/rewardNeuronScreen_round2/blueBackLight-level3/"
// expDir = "5xCsChr/5xCsChr_x_HC-Gal4_female/luLEDTraces/"

//----------------------------
setBatchMode(true);
source = getDirectory("Choose Source Directory");
process(source);

print("DONE!");

function process(baseDir) {
   folderList = getFileList(baseDir)
   
   for (f=0; f<folderList.length; f++) {
      expDir = folderList[f];
      print(expDir);
      
      dataDir =  baseDir + expDir + File.separator;
      
      if (!File.exists(dataDir + "firstFrames.csv")) { //folder with luLED traces already exists
       	 print("LED traces have not yet been extracted. Please run findFirstAssyFrame_UFMF_batch.ijm and startFrameFromLEDTrace_UFMF.py.");
      }
      else{ //data file exists
      	
      	 frameSaveDir = "stimFrames/";
		 File.makeDirectory(dataDir + frameSaveDir);

		 // Read in firstFrames.csv and iterate through all files listed in there
		 print("opening csv: " + dataDir + "firstFrames.csv");
		 open(dataDir + "firstFrames.csv"); //now in "Results" table

		 headings = split(String.getResultsHeadings);
		 
		 for (row = 0; row < nResults; row++) { //each row corresponds to one movie
		 	
    		fileName = getResultString(headings[1],row); //first results column is unncesseary, just work around for a fiji bug
    		fileNameShort = substring(fileName,0,lengthOf(fileName)-41);
    
    		print(fileNameShort);
    		analysisDir = baseDir + expDir + frameSaveDir + fileNameShort + File.separator;
    		File.makeDirectory(analysisDir);

    		startFrame = getResult(headings[2],row);
    		print(startFrame);

    		//load movie
    		run("Import UFMF", "choose=" + baseDir + expDir + fileName + ".ufmf");

    		//generate array of frames that need to be saved
    		fps = 30;
    		stimDuration = 30;
    		pauseDuration = 10;
    		shiftF = 5;
    
	    	frame1 = startFrame + 1;
    		frame2 = startFrame + fps * stimDuration - shiftF;
    		frame3 = frame2 + fps * (stimDuration+pauseDuration) - shiftF;
    		frame4 = frame3 + fps * (stimDuration+pauseDuration) - shiftF;
    		frame5 = frame4 + fps * (stimDuration+pauseDuration) - shiftF;
    		frame6 = frame5 + fps * (stimDuration+pauseDuration) - shiftF;
    		frame7 = frame6 + fps * (stimDuration+pauseDuration) - shiftF;
    
    		framesToSelect = newArray(frame1,frame2,frame3,frame4,frame5,frame6,frame7);
    
    		for (i=0; i<framesToSelect.length; i++) {
    			currFrame = framesToSelect[i];
    			setSlice(currFrame);
    			run("Duplicate...", "duplicate range=" + currFrame + "-" + currFrame);
    			saveAs("Jpeg", analysisDir + "frame_" + currFrame + ".jpg");
    			close("frame_" + currFrame + ".jpg");
    		}
    
    		run("Close All");
    		run("Collect Garbage");
    
		 } //iterate through movies
           
      } //experiment to analyse

      print("done: " + baseDir + expDir); 
      run("Close All");
      run("Collect Garbage");
   } //iterate through folders in base directory
   
} //function def

setBatchMode(false);