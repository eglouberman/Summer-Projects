The following program is a very powerful program, since it has the capability of deleting many many files. I recommend trying it out on a couple of files first to see if it works, and then moving to larger quantities. 

Directions: 

Place Cleaner.py into the top level directory of where you want your "log" files to be deleted. 

Cleaner.py will iterate through all of the files in the same directory, plus ALL the ones in the lower directories. It will delete all files with a suffix _log before a certain date. 


Input into the command line in the same directory as Cleaner.py: 

python Cleaner.py DAYS

where 'DAYS' is the number of days in the past that is set as a marker for everything to be deleted before those days. For example, if you input 365, every file ending in 'logs' that was created a year ago is SAVED, and all the ones that were created longer than a year ago are deleted. 
 