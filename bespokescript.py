# Script to search for calls to bespoke loggers in ep_engine and replace with a new logfmt call (spdlog style)
# Will require some manual intervention to fix the function definitions

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

        pattern = re.compile('log\(.*?;', re.DOTALL)
        for m in re.finditer(pattern, read_data):
            s = m.group(0)
            methodpattern = re.compile('(log\(EXTENSION_LOG_(.*?)),.*?"', re.DOTALL)

            for methodm in re.finditer(methodpattern, m.group(0)):
                if methodm.group(2) == 'NOTICE':
                    s = s.replace(methodm.group(1), 'logfmt(spdlog::level::level_enum::info')
                elif methodm.group(2) == 'WARNING':
                    s = s.replace(methodm.group(1), 'logfmt(spdlog::level::level_enum::warn')
                elif methodm.group(2) == 'INFO':
                    s = s.replace(methodm.group(1), 'logfmt(spdlog::level::level_enum::debug')
                elif methodm.group(2) == 'FATAL':
                    s = s.replace(methodm.group(1), 'logfmt(spdlog::level::level_enum::critical')
                else:
                    s = s.replace(methodm.group(1), 'logfmt(spdlog::level::level_enum::' + methodm.group(2).lower())

            methodpattern = re.compile('log\(.*EXTENSION_LOG_(.*?)?,', re.DOTALL)
            for methodm in re.finditer(methodpattern, m.group(0)):
                if methodm.group(1) == 'NOTICE':
                    s = s.replace(methodm.group(0), 'logfmt(spdlog::level::level_enum::info,')
                elif methodm.group(1) == 'WARNING':
                    s = s.replace(methodm.group(0), 'logfmt(spdlog::level::level_enum::warn,')
                elif methodm.group(1) == 'INFO':
                    s = s.replace(methodm.group(0), 'logfmt(spdlog::level::level_enum::debug,')
                elif methodm.group(1) == 'FATAL':
                    s = s.replace(methodm.group(0), 'logfmt(spdlog::level::level_enum::critical,')
                else:
                    s = s.replace(methodm.group(0), 'logfmt(spdlog::level::level_enum::' + methodm.group(1).lower())

            if "log(EXTENSION" in s:
                print "&&&& LOG( function still called, manual intervention required"
                print s

            parampattern = re.compile('(%(%?(d|f|s|p|ld|lu|u|zu|X|[.*s]|"|zd)))')
            for paramm in re.finditer(parampattern, m.group(0)):
                if "\"" in paramm.group(0):
                    s = s.replace(paramm.group(0), '{}"')
                else:
                    s = s.replace(paramm.group(0), '{}')

            if "%" in s:
                print "**** Missing printf param type"
                print s

            pripattern = re.compile('"[ |]PRI.*?"', re.DOTALL)
            for prim in re.finditer(pripattern, m.group(0)):
                s = s.replace(prim.group(0), '')

            pripattern = re.compile('"([ |]PRI.*?)["|,]', re.DOTALL)
            for prim in re.finditer(pripattern, m.group(0)):
                s = s.replace(prim.group(1), '')

            vbpattern = re.compile("(vbucket:{})", re.DOTALL)
            for vbm in re.finditer(vbpattern, s):
                s = s.replace(vbm.group(1), 'vb:{}')

            vbpattern = re.compile("(vbucket {})", re.DOTALL)
            for vbm in re.finditer(vbpattern, s):
                s = s.replace(vbm.group(1), 'vb:{}')

            vbpattern = re.compile("(vb {})", re.DOTALL)
            for vbm in re.finditer(vbpattern, s):
                s = s.replace(vbm.group(1), 'vb:{}')

            if ".c_str()" in s:
                s = s.replace(".c_str()", '')

            #print s
            read_data = read_data.replace(m.group(0), s)

        #print read_data
        f.closed

    with open(filename, 'w+') as fnew:
        fnew.write(read_data)
        fnew.closed
