import re
from hanziconv import HanziConv

# Converts charlist.csv (credit to https://words.hk/faiman/analysis/charlist/) to a 2D string array literal 
# in jyutping.h, so that the pronunciations are directly compiled into the executable

class Hanzi:
    def __init__(self, char, jyutpings):
            self.char = char
            jyutpings = [(jyutping[0], int(jyutping[1])) for jyutping in jyutpings] # convert 'commanality' score to int so it can be sorted
            self.jyutpings = jyutpings
            self.jyutpings.sort(key=lambda x: x[1], reverse=True) # sort by 'commonality' score

    def __lt__(self, other):
        return self.char < other.char

lines = []
with open('charlist.csv', "r") as file:
    lines = file.readlines()

hanzis = []
for i in range(1, len(lines)):
    line_split = lines[i].split(',', 1)
    char = line_split[0]
    jyutpings = re.findall('""([^"]*)"":\s+(\d+)', line_split[1])
    hanzis.append(Hanzi(char, jyutpings))
    charSimplified = HanziConv.toSimplified(char)
    if (charSimplified != char): # if simplified variant exists, add it too
        hanzis.append(Hanzi(charSimplified, jyutpings))
hanzis.sort(key=lambda x: x.char, reverse=False) # sort by unicode

out = "const int PRONUNCIATIONS_LENGTH = " + str(len(hanzis)) + ";\n"
out += "char* PRONUNCIATIONS[][2] =\n{\n"
for hanzi in hanzis:
    out += "\t{ "
    out += "\"" + hanzi.char + "\"" + ", "
    out += "\"" + ":".join([jyutping[0] for jyutping in hanzi.jyutpings]) + "\""
    out += " },\n"
out = out[0:len(out) - 2] + "\n" # remove extra ',' and replace newline
out += "};"

with open('jyutping.h', "w") as file:
    file.write(out)