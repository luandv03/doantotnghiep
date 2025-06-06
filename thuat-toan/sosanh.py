import matplotlib.pyplot as plt
import pandas as pd

# Danh sách 30 lời giải
data = [
    (7, 71, 602563.5), (9, 63, 596431.0), (7, 75, 603878.0), (4, 84, 612095.0),
    (7, 75, 602519.5), (7, 76, 573199.0), (8, 74, 610588.0), (8, 70, 621654.0),
    (8, 75, 607348.5), (7, 75, 587455.0), (8, 74, 605737.0), (8, 74, 604521.5),
    (7, 75, 599164.5), (8, 78, 598042.5), (7, 75, 605671.0), (8, 74, 611633.0),
    (8, 76, 612870.5), (8, 71, 599434.0), (7, 71, 588379.0), (7, 73, 595738.0),
    (7, 75, 606897.5), (7, 71, 594121.0), (8, 71, 616654.5), (6, 84, 613937.5),
    (5, 92, 616302.5), (7, 67, 614526.0), (7, 75, 601909.0), (8, 71, 595958.0),
    (8, 85, 612496.5), (7, 76, 606919.5)
]

# Tạo DataFrame
df = pd.DataFrame(data, columns=["Completed Orders", "Total Shifts", "Total Cost"])

# Trực quan hoá: scatter 2D với màu đại diện cho Total Shifts
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    df["Completed Orders"],
    df["Total Cost"],
    c=df["Total Shifts"],
    cmap="viridis",
    s=100,
    edgecolor='k'
)

plt.colorbar(scatter, label="Total Shifts")
plt.xlabel("Completed Orders On Time")
plt.ylabel("Total Cost")
plt.title("Harmony Search Result Visualization")
plt.grid(True)
plt.tight_layout()
plt.show()
