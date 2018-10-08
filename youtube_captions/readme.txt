The following program utilizes API youtube-dl in order to download wav forms of videos from youtube including their subtitles. The output is a txt file that has subtitles and a given wav file with the same name in order to train machine learning speech recognition language models. 

Dependencies: 
In order to make this work, you need to install youtube-dl. You can do so using pip. 

Directions: 
In the "youtube_captions" folder, you will see a txt file called url.txt
For all the videos that you want downloaded, please copy and paste their URL's into each line, making sure each line consists of only one URL. 

Open the command line and cd into the top level directory. 
Type the following: 
	python youtube_extractor.py url.txt

The output will be consecutive files ending in txt and wav that are arranged properly to put through a language model. 


 