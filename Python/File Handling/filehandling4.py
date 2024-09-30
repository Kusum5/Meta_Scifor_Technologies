file = open("serial.txt", "r")
lines = file.readlines()
file = open("serial.txt","w")
for i,line in enumerate(lines,start =1):
    file.write(f"{i}. {line}")