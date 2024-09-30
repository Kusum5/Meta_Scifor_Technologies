f = open("numericalFile.txt","r")
lines = f.read()
words = lines.split()
for i,word in enumerate(words):
    if word.isnumeric():
        print(i+1)