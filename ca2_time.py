import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime

# Define the tasks and their start and end dates
tasks = {
    "Candidate Stage Assessment 2": ("2023-11-27", "2023-12-01"),
    "Chapter 4B (Contrast Modelling in Sections)": ("2023-11-01", "2023-11-30"),
    "Chapter 4C and Chapter 5 (Part 1)": ("2023-12-01", "2023-12-30"),
    "Chapter 5 (Part 2)": ("2024-01-01", "2024-01-30"),
    "Chapter 6 (Analysis of Genuine Music Outliers)": ("2024-02-01", "2024-03-30"),
    "Chapter 7 and 8 (Discussion and Conclusion)": ("2024-04-01", "2024-04-30"),
    "Candidate Stage Assessment 3": ("2024-05-01", "2024-05-10"),
    "Proofreading": ("2024-05-11", "2024-07-14"),
    "Submit Final Thesis": ("2024-07-15", "2024-07-15")
}

# Convert the date strings to datetime objects
for task, (start, end) in tasks.items():
    tasks[task] = (datetime.datetime.strptime(start, "%Y-%m-%d"),
                   datetime.datetime.strptime(end, "%Y-%m-%d"))

# Create a list of task names and their start and end dates
names = list(tasks.keys())
dates = list(tasks.values())

# Create a figure and axis for the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

# Add tasks to the Gantt chart
for i, (name, (start, end)) in enumerate(zip(names, dates)):
    ax.barh(name, (end - start).days, left=start, height=0.4, align='center')

# Format the x-axis to show dates
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)

# Set labels and title
ax.set_xlabel("Date")
ax.set_ylabel("Task")
ax.set_title("Gantt Chart Timeline")

# Show the Gantt chart
plt.tight_layout()
plt.show()
