import re

file = open("textfile.txt","r")
x = file.read()
y = re.sub(r'(\d+)\.', r'\1.\n',x)

file = open("textfile.txt","a")
file.write(y)
