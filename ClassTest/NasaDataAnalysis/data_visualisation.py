import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'Stars.csv'
data = pd.read_csv(file_path)

data[['Temperature','L','R','A_M','Color','Spectral_Class','Type']].hist(figsize=(10,5))
plt.suptitle('Feature')
plt.show()

print()

plt.figure(figsize=(10,6))
sns.countplot(data = data, x='Color',order=data['Color'].value_counts().index)
plt.xticks(rotation=50)
plt.title("Distribution based on Color")
plt.show()
