The following program implements API PDffigures2 and Scala and retrieves the captions and figures for any list of publications. The use for this is for speech recognition services. 

You may need to have Scala and API “Pdffigures2” installed onto your computer. You can view how to do so here: https://stackoverflow.com/questions/45951477/how-to-install-scala-software

If it already works with the files I have attached, then you do not need to install it.

You’re also going to need to download and configure AWS through the command line. The documentation can be seen here: https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html

Next, move all the desired PDF’s to be extracted into the “pdfs” folder. 

cd into pdffigures2 and run “python figure_mapper.py” on the Terminal. figure_mapper.py, when run, will return a dictionary in the following format: 

img_dict
{
NameOfFigure : [[arrayOfPixelsforFigure], string of said caption for the figure, array of wave info from Polly description of caption]
…
}

The images will also be stored into the “images” folder in .png format. 

The wave files will be stored in the “audios” folder in .wav format. 
