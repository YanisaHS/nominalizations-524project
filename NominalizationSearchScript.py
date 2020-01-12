import spacy
import nltk.app.wordnet_app as wnapp
from nltk.corpus import wordnet as wn

# Part One: Create function to search for nominalizations with NLTK

# Save final nominalizations of words into a dictionary (rather than list) for caching/efficiency
listOfNominalizedWords = {}
finalNounsAndCorrespondingVerbs = {}
knownNotNominalizations = {}
def nominalizationFunction(word):
    if word in finalNounsAndCorrespondingVerbs:
        return True
    if word in knownNotNominalizations:
        return False
    # Parse for synsets which match "word" (noun) - the synsets picked up will also be nouns
    nounSynsets = wn.synsets(word, pos=wn.NOUN)
    # List the lemmas of the synsets we just identified - these lemmas are still nouns
    for synset in nounSynsets:
        lemmas = synset.lemmas()
        # Find all lemmas which are "derivationally related" - these will be different syntactic categories
        for lemma in lemmas:
            listOfDRF = lemma.derivationally_related_forms() 
            for individualWordInDRF in listOfDRF:
                wordKey = individualWordInDRF.key()
                # ^^Creates the WN Key as a string
                splitStringWordKey = wordKey.split("%")
                splitStringIndex = splitStringWordKey[0]
                # Parsing for nominalizations - must be verbs and match first 3 characters
                if splitStringWordKey[1][0] != "1" and splitStringIndex[0:3] == word[0:3]:
                    if len(splitStringIndex) <= len(word):
                        finalRoots = wordKey.partition("%")[0]
                        # Add nominalizations to lists to track frequency & words
                        nomTracker(word)
                        finalNounsAndCorrespondingVerbs[word] = finalRoots
                        return True
                        # If nominaliztion is found, function ends here because it does not have to
                        #   check the other words (it doesn't matter)
    knownNotNominalizations[word] = ""
    return False

# Below function is to keep track of what words are nominalizations and their frequencies

def nomTracker(word):
    if word in listOfNominalizedWords:
        listOfNominalizedWords[word] = listOfNominalizedWords[word] + 1
    else:
        listOfNominalizedWords[word] = 1

# Part Two: Open NOMLEX-PLUS as a list and cache it

cachedNOMLEXPLUS = set()
openNOMLEXPLUS = open("/Users/yanisa/GoogleDrive/Data/cleanNOMLEXPLUS.txt")
print("Loading texts...")
for individualWordInNOMLEX in openNOMLEXPLUS:
    # Removie the formatting for a new line
    individualWordInNOMLEX = individualWordInNOMLEX.rstrip("\n")
    cachedNOMLEXPLUS.add(individualWordInNOMLEX)

# Part Three: Run nlp function in spaCy on text to POS-tag it

openTextFile = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 524 English Structure/Texts/VisualPerformingArtsTexts.txt", "r")
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 8000000
textSamples = nlp(openTextFile.read())
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
        if wordInSample.text in cachedNOMLEXPLUS:
            totalNumberOfNominalizations = totalNumberOfNominalizations + 1
            # Count the number of nominalizations which match in NOMLEX PLUS
            nomTracker(wordInSample.text)

# Part Five: For nouns not captured in NOMLEX PLUS, parse through NLTK to see if they are nominalizations

        else:
            if nominalizationFunction(wordInSample.text) == True:
                totalNumberOfNominalizations = totalNumberOfNominalizations + 1

print("The total number of words is: ", totalWords)
print("The total number of nouns is: ", totalNouns)
print("The total number of nominalizations is: ", totalNumberOfNominalizations)
print("The total frequency of nominalizations in the text is: ", totalNumberOfNominalizations / totalWords)