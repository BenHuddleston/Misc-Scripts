# Script to fix log messages that make a macro call and prefix a pre-defined prefix manually instead of using the logger

import re
import os

filepath = '/Users/benhuddleston/Documents/couchbase/source/kv_engine/engines/ep'

def getfiles(filepath):
    files = [];
    for filename in os.listdir(filepath):
        if os.path.isdir(filepath + '/' + filename):
            files.extend(getfiles(filepath + '/' + filename))
        else:
            files.append(filepath + '/' + filename)
    return files

print getfiles(filepath)

for filename in getfiles(filepath):
    if not filename.endswith(".cc"):
        continue

    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    print filename
    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"

    read_data = ""
    with open(filename, 'r+') as f:
        read_data = f.read()

        pattern = re.compile('EP_LOG_[A-Z]*\(.*?;', re.DOTALL)
        for m in re.finditer(pattern, read_data):
            s = m.group(0)

            blheaderpattern = re.compile(',\s*bucketLogHeader\(\)', re.DOTALL)
            for blheaderm in re.finditer(blheaderpattern, m.group(0)):
                s = s.replace("EP_LOG_", "bucketLogger->")
                s = s.replace(blheaderm.group(0), "")

                sevpattern = re.compile('EP_LOG_([A-Z]+?\()')
                for sevm in re.finditer(sevpattern, m.group(0)):
                    s = s.replace(sevm.group(1), sevm.group(1).lower())

                parampattern = re.compile("{} ")
                for paramm in re.finditer(parampattern, m.group(0)):
                    s = s.replace (paramm.group(0), "")
                    break;

                print s


            read_data = read_data.replace(m.group(0), s)

        f.closed

    with open(filename, 'w+') as fnew:
        fnew.write(read_data)
        fnew.closed
