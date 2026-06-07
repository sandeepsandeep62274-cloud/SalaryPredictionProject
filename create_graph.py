import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("salary_data.csv")

plt.figure(figsize=(8,5))

plt.plot(
    data["YearsExperience"],
    data["Salary"],
    marker="o"
)

plt.title("Experience vs Salary")

plt.xlabel("Years Of Experience")

plt.ylabel("Salary")

plt.grid(True)

plt.savefig("static/graph.png")

plt.close()

print("Graph Created Successfully!")