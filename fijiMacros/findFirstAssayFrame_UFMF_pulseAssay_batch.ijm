setBatchMode(true);
source = getDirectory("Choose Source Directory");
process(source);
print("All done.");

function process(dirIn) {
   folderList = getFileList(dirIn)
   
   for (f=0; f<folderList.length; f++) {
      expFolder = folderList[f];
      print(expFolder);
      saveDir =  dirIn + expFolder + "luLEDTraces" + File.separator;

      list = getFileList(dirIn + File.separator + expFolder);

      if (File.exists(saveDir)) { //folder with luLED traces already exists
       	 print("LED traces already extracted for this folder");
   
      }else{
         for (i=0; i<list.length; i++) {
      	    fileNameUFMF = list[i];
         
            if (endsWith(list[i], ".ufmf")) {
               showProgress(i+1, list.length);

               if(! File.exists(saveDir)) {
               		File.makeDirectory(saveDir);
               }

               fileName = substring(fileNameUFMF,0,lengthOf(fileNameUFMF)-5);
               fnIn = dirIn + expFolder + fileName;
            
               run("Import UFMF", "choose=" + fnIn + ".ufmf");
	           print("opened " + fileName);

	           makeRectangle (8, 0, 25, 25); //142, 10, 25, 25, (2,2, 25, 25);  //marks left upper indicator LED (previous 135, 0, 25, 25)  (10, 1, 25, 25)
	    
	           selectWindow(fileName + ".ufmf");
	           run("Plot Z-axis Profile");
	    
	           saveAs("Results", saveDir + fileName + "_luLEDTrace.csv");

	           close("Results");
	           if (isOpen("Results")) {
		          selectWindow("Results");
		          run("Close");
	           }
	           close(fileName + ".ufmf");

	           print("done: " + dirIn + expFolder); 
            }
         }
      }
      run("Close All");
      run("Collect Garbage");
   }
}
setBatchMode(false);

//now use python script to extract first frames and write those to file...

