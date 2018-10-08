The following program enables a written command in the console to download and parse publications by any given author from the internet, and create text files filled with meaningful sentences ready to train machine learning language models. 

Directions: 

First, download Pdftotext library using brew or pip. 
Install scrapy using pip or going on the scrapy.io website. 

Unzip the project into preferred directory. 
Open the command line, and cd into the top level directory. 
Next, type in the following command: 

python pub_crawler.py First_name Last_name

where first_name and last name (not case_sensitive) are the given author you want to download. The resulting output should be text files with the prefix new_...txt files created in the very same directory. 

