text = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/WritingTextFile.txt", "r")
data = text.read()
text.close()

words = data.split(" ")
wordCount = len(words)
print("Word Count: ", wordCount)