import matplotlib.pyplot as plt
import csv
import os

# Read the CSV file
real_x = []
real_y = []
pred_x = []
pred_y = []

file_path = os.path.expanduser('~/motion_data.csv')

print(f"Reading data from {file_path}...")

with open(file_path, 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots) # Skip header row
    for row in plots:
        real_x.append(float(row[1]))
        real_y.append(float(row[2]))
        pred_x.append(float(row[3]))
        pred_y.append(float(row[4]))

# Plotting
plt.figure(figsize=(10, 6))

# Plot Real Path (Green)
plt.plot(real_x, real_y, label='Odometry (Real)', color='green', linewidth=2)

# Plot Predicted Path (Red Dashed)
plt.plot(pred_x, pred_y, label='Velocity Model (Predicted)', color='red', linestyle='--')

plt.title('Motion Model Comparison')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.legend()
plt.grid(True)
plt.axis('equal') # Important to see the curve correctly
plt.show()
