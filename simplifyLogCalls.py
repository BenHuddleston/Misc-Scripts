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

        pattern = re.compile('bucketLogger.(log\([\n\s*|]*spdlog::level::level_enum::([a-z]*),).*?;', re.DOTALL)
        for m in re.finditer(pattern, read_data):
            s = m.group(0)

            s = s.replace(m.group(1), m.group(2) + '(')
            print s

            read_data = read_data.replace(m.group(0), s)

        f.closed

    with open(filename, 'w+') as fnew:
        fnew.write(read_data)
        fnew.closed
