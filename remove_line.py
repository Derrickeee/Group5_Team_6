import re

infile = "../samples/test.smali"
outfile = "../samples/test_removed_line.smali"

with open(infile) as fin, open(outfile, "w+") as fout:
    for line in fin:
        if re.search('line\s\d', line):
            line = line.replace(line, "")
        fout.write(line)
