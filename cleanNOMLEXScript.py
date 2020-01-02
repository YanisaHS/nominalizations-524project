textFileNOMLEX = open("/Users/yanisa/Google Drive/Data/NOMLEX-plus.1.0.txt")
getNouns = []
for line in textFileNOMLEX:
    if line.startswith("(NOM :ORTH"):
        splitStringForNouns = line.split("\"")
        finalNoun = splitStringForNouns[1]
        if finalNoun[-1].isnumeric():
            finalNoun = finalNoun[:-1]
        getNouns.append(finalNoun)

makeTxtFile = open("/Users/yanisa/Google Drive/Data/cleanNOMLEXPLUS.txt", "w")
for noun in getNouns:
    makeTxtFile.write(noun + "\n")