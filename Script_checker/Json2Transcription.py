import json
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def parse_line(string_format_line):
    _speakers = ''
    _content = ''
    string_format_line = string_format_line.replace('</t>', '<t>')
    if '<t>' not in string_format_line:
        return "{:<30}".format('NO_SPEAKER'), string_format_line

    b = string_format_line.split('<t>')
    for i in range(1, len(b)):
        if i % 2 == 1:
            _speakers += b[i]
        else:
            _content += b[i]
    _speakers = _speakers.replace(':', '_').replace(' ', '').replace(',', '_')[:-1]
    _content = _content.replace('<br><br>', ',').replace('<br>', '')
    print ('speakers: ' + _speakers)
    print ('content : ' + _content)
    for c in _content:
        if ord(c) == 9835:
            _content = _content.replace(c, '')
    _speakers = "{:<30}".format(_speakers)
    return _speakers, _content

def parse_line_CHICAGO(string_format_line):
    _speakers = ''
    _content = ''
    string_format_line = string_format_line.replace('</t>', '<t>')
    if '<t>' not in string_format_line:
        return "{:<30}".format('NO_SPEAKER'), string_format_line

    b = string_format_line.split('<t>')
    for i in range(1, len(b)):
        if i % 2 == 1:
            _speakers += b[i]
        else:
            _content += b[i]
    _speakers = _speakers.replace(':', '_').replace(' ', '').replace(',', '_')[:-1]
    _content = _content.replace('<br><br>', ',').replace('<br>', '')
    print ('speakers: ' + _speakers)
    print ('content : ' + _content)
    for c in _content:
        if ord(c) == 9835:
            _content = _content.replace(c, '')
    _speakers = "{:<30}".format(_speakers)
    return _speakers, _content


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s json file'
        print 'eg. %s phantom_of_the_opera/poto.json'
        sys.exit(1)
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)

    #pprint(data)
    file = open(sys.argv[1].replace('.json', '_closedCaption.txt'), 'w')
    english = open(sys.argv[1].replace('.json', '_transcription.txt'), 'w')
    print(data['rows'][1]['text']['spa'])
    i = 0
    for line in data['rows']:
        print(i, line['text']['spa'].decode())
        speakers, content = parse_line(line['text']['spa'].decode('utf-8'))  # .encode('utf-8'))
        to_print = str(i) + '\t' + speakers + '\tbegin_time\tend_time\t' + content + '\n'
        file.write(to_print)
        i += 1
        splt = to_print.split('\t')
        if splt[1].strip() == 'NO_SPEAKER':
            continue
        ignoreFlag = False
        newText = ""
        for letter in splt[4]:
            if letter == '(':
                ignoreFlag = True
                continue
            if letter == ')':
                ignoreFlag = False
                continue
            if ignoreFlag == True:
                continue
            if ignoreFlag == False:
                newText += letter
                continue
            if newText == '\n':
                continue
        newLine = '\t'.join([splt[0], splt[1], splt[2], splt[3], newText.lstrip().strip('\n')])+'\n'
        english.write(newLine)
    print('Done')

