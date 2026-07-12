#!/usr/bin/env python3
"""Plot logged odometry vs. velocity-model motion data from a CSV file.

Usage:
    ros2 run my_yolo_system plot_csv [path/to/motion_data.csv]
    python3 plot_csv.py [path/to/motion_data.csv]

Defaults to ``~/motion_data.csv`` when no path is given. The CSV is expected
to have a header row followed by columns:
    <index>, real_x, real_y, pred_x, pred_y
"""

import argparse
import csv
import os

import matplotlib.pyplot as plt


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'csv_path',
        nargs='?',
        default=os.path.expanduser('~/motion_data.csv'),
        help='Path to the motion data CSV (default: ~/motion_data.csv)',
    )
    parser.add_argument(
        '--save',
        default=None,
        help='Save the plot to this image path instead of showing a window '
             '(useful for headless/CI runs).',
    )
    parsed = parser.parse_args(args=args)
    file_path = os.path.expanduser(parsed.csv_path)

    real_x, real_y, pred_x, pred_y = [], [], [], []

    print(f"Reading data from {file_path}...")

    with open(file_path, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots)  # Skip header row
        for row in plots:
            real_x.append(float(row[1]))
            real_y.append(float(row[2]))
            pred_x.append(float(row[3]))
            pred_y.append(float(row[4]))

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(real_x, real_y, label='Odometry (Real)', color='green', linewidth=2)
    plt.plot(pred_x, pred_y, label='Velocity Model (Predicted)', color='red',
             linestyle='--')

    plt.title('Motion Model Comparison')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')  # Important to see the curve correctly

    if parsed.save:
        plt.savefig(parsed.save, dpi=120, bbox_inches='tight')
        print(f"Saved plot to {parsed.save}")
    else:
        plt.show()


if __name__ == '__main__':
    main()
