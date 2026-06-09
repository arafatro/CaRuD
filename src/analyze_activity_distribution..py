import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
file_path = 'data/BPI_Challenge_2019.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Count the distribution of activities
activity_counts = df['concept:name'].value_counts()

# Print all activity names and their occurrence counts
print("All activity names and their occurrence counts:")
print(activity_counts)

# Plot bar chart
plt.figure(figsize=(18, 8))
activity_counts.plot(kind='bar')

plt.title('Activity Distribution', fontsize=16)
plt.xlabel('Activity Name', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(rotation=75, ha='right')  # Tilt X-axis labels to prevent overlap
plt.tight_layout()

plt.show()
