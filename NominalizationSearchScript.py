import spacy
import nltk.app.wordnet_app as wnapp
from nltk.corpus import wordnet as wn

# Part One: Create function to search for nominalizations with NLTK

listOfNominalizedWords = {}
finalNounsAndCorrespondingVerbs = {}
knownNotNominalizations = {}
# Save final nominalizations of words into a dictionary (rather than list) for caching/efficiency
def nominalizationFunction(word):
    # print("Looking for nominalizations...")
    if word in finalNounsAndCorrespondingVerbs:
        return True
    if word in knownNotNominalizations:
        return False
    nounSynsets = wn.synsets(word, pos=wn.NOUN)
    # Parse for synsets which match "word" (noun) 
    # The synsets picked up with also be nouns
    for synset in nounSynsets:
        lemmas = synset.lemmas()
        # List the lemmas of the synsets we just identified
        # These lemmas are still nouns
        for lemma in lemmas:
            listOfDRF = lemma.derivationally_related_forms() 
            # Find all lemmas which are "derivationally related"
            # Different syntactic categories
            for individualWordInDRF in listOfDRF:
                wordKey = individualWordInDRF.key()
                # Creates the WN Key as a string
                splitStringWordKey = wordKey.split("%")
                splitStringIndex = splitStringWordKey[0]
                if splitStringWordKey[1][0] != "1" and splitStringIndex[0:3] == word[0:3]:
                    if len(splitStringIndex) <= len(word):
                    # Parsing for nominalizations - must be verbs and match first 3 characters
                        finalRoots = wordKey.partition("%")[0]
                        # Create the list of verbs which are can create nominalizations of the word
                        nomTracker(word)
                        finalNounsAndCorrespondingVerbs[word] = finalRoots
                        return True
                        # If nominaliztion is found, function ends here because it does not have to
                        #   check the other words (it doesn't matter)
    knownNotNominalizations[word] = ""
    # print("These are extra:", knownNotNominalizations)
    return False

# Below function is to keep track of what words are nominalizations and their frequencies

def nomTracker(word):
    if word in listOfNominalizedWords:
        listOfNominalizedWords[word] = listOfNominalizedWords[word] + 1
    else:
        listOfNominalizedWords[word] = 1

# Part Two: Open NOMLEX-PLUS as a list and cache it

cachedNOMLEXPLUS = set()
openNOMLEXPLUS = open("/Users/yanisa/Google Drive/Data/cleanNOMLEXPLUS.txt")
print("Loading texts...")
for individualWordInNOMLEX in openNOMLEXPLUS:
    individualWordInNOMLEX = individualWordInNOMLEX.rstrip("\n")
    # Removing the formatting for a new line
    cachedNOMLEXPLUS.add(individualWordInNOMLEX)

# Part Three: Run nlp function in spaCy on text to POS-tag it

openTextFile = open("/Users/yanisa/Google Drive/School/Homework - Grad School/UofA/EN 524 English Structure/Texts/VisualPerformingArtsTexts.txt", "r")
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 8000000
textSamples = nlp(openTextFile.read())
# for token in textSamples:
    # print(token.pos_, token.text)
print("Files uploaded and POS-tagged.")

# Part Four: Search for nouns and compare nouns to list of nominalizations in NOMLEX PLUS

totalNumberOfNominalizations = 0
totalWords = 0
totalNouns = 0
for wordInSample in textSamples:
    if wordInSample.pos_ == "SYM" or wordInSample.pos_ == "PUNCT":
        continue
    if wordInSample.pos_ == "NUM" and wordInSample.text.isnumeric():
        continue
    if wordInSample.pos_ == "X":
        continue
    if wordInSample.pos_ == "SPACE":
        continue
    totalWords = totalWords + 1
    if wordInSample.pos_ == "NOUN":
        totalNouns = totalNouns + 1
        #if (wordInSample.text.endswith("s") or wordInSample.text.endswith("es")) and (not wordInSample.text.endswith("ings")):
            #continue
            # continue brings it back up to re-start the loop
        if wordInSample.text in cachedNOMLEXPLUS:
            totalNumberOfNominalizations = totalNumberOfNominalizations + 1
            nomTracker(wordInSample.text)
            # Counted the number of nominalizations which match in NOMLEX PLUS

# Part Five: For nouns not captured in NOMLEX PLUS, parse through NLTK to see if they are nominalizations

        else:
            if nominalizationFunction(wordInSample.text) == True:
                totalNumberOfNominalizations = totalNumberOfNominalizations + 1

# print(finalNounsAndCorrespondingVerbs)
print("The total number of words is: ", totalWords)
print("The total number of nouns is: ", totalNouns)
print("The total number of nominalizations is: ", totalNumberOfNominalizations)
print("The total frequency of nominalizations in the text is: ", totalNumberOfNominalizations / totalWords)
 
# listOfNominalizedWordsForCSV = open("/Users/yanisa/Google Drive/School/Homework - Grad School/UofA/EN 524 English Structure/FrequencyData/VisualPerformingArtsCSVData.csv", "w")
# for word, frequency in listOfNominalizedWords.items():
#     listOfNominalizedWordsForCSV.write(word + "," + str(frequency) + "\n")

