# Script to merge two phosphor trace files
import argparse
import re


def getFile(file):
    print ("Reading file '" + file + "'")
    with open(file, "r") as f:
        return f.readlines()

def writeFile(file, lines):
    with open(file, "w") as f:
        f.writelines(lines)

def removeEventsForThread(fileName, fileData, threads):
    tids = []
    lines = []
    pattern = re.compile("\"tid\": [0-9]+")
    for line in fileData:
        if "thread_name" in line:
            for threadName in threads:
                if threadName in line:
                    for m in re.finditer(pattern, line):
                        tids.append(m.group(0).replace(" ", ""))
                    #fileData.remove(line)
                    break
                else:
                    lines.append(line)
        else:
            if not any((tid in line) for tid in tids):
                lines.append(line)

    print (tids)

    return lines

def merge(files):
    started = False

    lines = []
    traceEvents = "  \"traceEvents\": [\n"
    lines.append("{\n")
    lines.append(traceEvents)
    for file in files:
        for line in files[file]:
            if "Started" in line:
                if not started:
                    started = True
                else:
                    continue
            if "    ]\n" == line or "}" == line or "{\n" == line or traceEvents == line:
                continue
            if line[-2] != ",":
                if file != list(files.keys())[-1]:
                    line = line.replace("\n", ",\n")
            lines.append(line)
    if lines[-1][-2] == ",":
        lines[-1] = lines[-1].replace(",\n", "\n")
    lines.append("    ]\n")
    lines.append("}")
    return lines

# --- Start Main Script ---
# Create argparser so the user can specify which job to search
argParser = argparse.ArgumentParser()
argParser.add_argument('files', type=str, nargs='+', help='Json trace files to be merged')
argParser.add_argument('--output', '-o', type=str, help='Output file. ', required=True)
argParser.add_argument('--removeThreads', '-r', type=str,
                       help='Remove events for the given thread names. ', action='append',required=False)

args = argParser.parse_args()
print (args)

if not args.files:
    print ("Must specify files")
    exit(0)

if len(args.files) != 2:
    print ("Invalid number of files")
    exit(1)

files = {}

for file in args.files:
    files[file] = getFile(file)

if args.removeThreads:
    print ("Removing events")
    for file in files:
        files[file] = removeEventsForThread(file,
                                            files[file],
                                            args.removeThreads)

print ("Merging files")
lines = merge(files)

writeFile(args.output, lines)
