import pandas as pd

file_path = 'Stars.csv'
data = pd.read_csv(file_path)
print("Headings")
print(data.head())

print()
print("Info")
print(data.info())

print()
print("Missing Data Values ")
print(data.isnull().sum())

print()
print("Description")
print(data.describe())

print("Types of Star Distribution")
print(data['Type'].value_counts())

