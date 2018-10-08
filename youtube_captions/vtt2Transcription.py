import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

def parse_line(lines, fle):
    sentenceList =[]
    count =0
    line =[]
    overall_sentence =""
    dontContinue = False
    for x in lines[4:]:
        if (dontContinue == False):
            nums = re.findall('(\d.[\d]*:\d.[\d]*:\d.[\d]*.\d.[\d]*)',x)
            if (len(nums)==0 and x != "\n"): #we are at a quote
                sentence = x[0:len(x)-1]
                sentence2 = re.sub("\n","", sentence)
                overall_sentence = overall_sentence + " " +sentence2
            elif (len(nums)==2): #we're at a number
                if (count>0):
                    sentenceList.append(overall_sentence)
                    line.append(overall_sentence)
                    to_write = "\t\t".join(line) +"\n"
                    overall_sentence = ""
                    fle.write(to_write) # we write the prev line
                count+=1
                line =[]
                ftr = [3600,60,1]
                j=sum([a*b for a,b in zip(ftr, map(float,nums[0].split(':')))])
                k=sum([a*b for a,b in zip(ftr, map(float,nums[1].split(':')))])
                line.append(str(count))
                line.append("SPEAKER")
                line.append(str(j))
                line.append(str(k))
    sentenceList.append(overall_sentence)
    line.append(overall_sentence)
    to_write = "\t\t".join(line) +"\n"
    overall_sentence = ""
    fle.write(to_write) # we write the prev line    
    print "DONE with transcription!" 


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s json file'
        print 'eg. %s phantom_of_the_opera/poto.json'
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = f.readlines()
#    with open('practice.vtt') as f:
#        lines = f.readlines()  
    #pprint(data)
    fle = open(sys.argv[1].replace('.vtt', '_closedCaption.txt'), 'w')
#    fle = open("practice.vtt".replace('.vtt', '_closedCaption.txt'), 'w')
    parse_line(lines, fle)
    
           
            
            

