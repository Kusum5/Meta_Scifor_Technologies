import datetime
f = open("bmi.txt", "a")
height_in_cm = int(input("Enter your height in cm: "))
height_in_m = height_in_cm *0.01
weight = int(input("Enter your weight in kg: "))
BMI = round(weight / (pow(height_in_m,2)),2)
print(BMI)
date = datetime.datetime.now()
f.write(f"{date}, {weight}kg, {height_in_m}m, BMI: {BMI}\n")