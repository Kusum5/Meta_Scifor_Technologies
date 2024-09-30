p = open("welcome.txt","r")
print(p)
print(p.read(),end="")

f1 = open("abc.txt","a")
for data in p:
    f1.write(data)