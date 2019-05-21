import argparse
import re

# Init commandline
parser = argparse.ArgumentParser(description='Specify file, get output.')

# Add input and output args
parser.add_argument("--input", "-i", type=str, required=True)
parser.add_argument("--output", "-o", type=argparse.FileType('w'), required=True)
args = parser.parse_args()

# Files
inputFile = args.input
outputFile = args.output

# Start parse
file = open(inputFile, "r")
parsedUrlList = []

# Parse line by line, manually, because logic
for line in file:
    if line.startswith('<?xml'):
        continue

    # Manually remove XML data structures because parsing is unreliable due to unfiltered data structures
    line = re.sub('<[^>]+>', '', line)

    # Strip anchors and query params
    line = line.split('?', 1)[0]
    line = line.split('#', 1)[0]

    # Strip return chars
    line = line.rstrip()

    # Strip trailing slashes
    line = line.rstrip("/")

    # Replace recurring IDs with {id} placeholder
    # IE /url/with/id/10 to /url/with/id/{id}
    line = re.sub('[/]+[0-9]{1,}$', '/{id}', line)

    # Only append if unique
    if line not in parsedUrlList:
        parsedUrlList.append(line)

file.close()

for line in parsedUrlList:
    outputFile.write(line + '\n')
