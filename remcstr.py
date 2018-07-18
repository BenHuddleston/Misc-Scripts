# Script to remove .c_str() instances from EP_LOG_ macro calls

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
            if ".c_str()" in s:
                s = s.replace(".c_str()", "")

        f.closed

    with open(filename, 'w+') as fnew:
        fnew.write(read_data)
        fnew.closed
