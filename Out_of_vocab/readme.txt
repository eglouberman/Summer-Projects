The following program takes an unknown dictionary word and finds the context in which this unknown word is used. This is used for language models and machine learning datasets in order to familiarize the AI with unknown words. 

Dependencies: 
Please install scrapy from the scrapy.io website or using pip 

Directions: 
On the command line, cd into the directory "findContext". 

Next, type in the following command: 

	scrapy crawl context -a word=WORD_HERE

Replace the word_here with the word you would like context for. The output will produce a file called WORD_HERE.txt with sentences in which the word_here is mentioned
