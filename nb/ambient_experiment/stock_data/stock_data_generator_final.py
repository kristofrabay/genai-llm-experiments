import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Set a random seed for reproducibility
np.random.seed(42)

# --- Segment 1: 0-30 sec (15 points) ---
# Stock hovers around 1000 USD with a variance of 5.
N = 0

n1 = 45
t1 = np.arange(0, n1, 2)  # 0,2,...,28 seconds
segment1 = np.random.normal(1000, 5, size=len(t1))
# Optionally, force the last value to be exactly 1000 for a smooth transition.
segment1[-1] = 1000

# --- Segment 2: 30-50 sec (10 points) ---
# Linear drop from 1000 to 920 USD.
N += n1
n2 = 20
t2 = np.arange(N, N + n2, 2)  # 30,32,...,48 seconds
segment2 = np.linspace(1000, 920, num=len(t2))

# --- Segment 3: 50-80 sec (15 points) ---
# Stock stays around 920 USD with low variance.
N += n2
n3 = 30
t3 = np.arange(N, N + n3, 2)  # 50,52,...,78 seconds
segment3 = np.random.normal(920, 5, size=len(t3))

# --- Segment 4: 80-140 sec (30 points) ---
# Stock gains gradually from 920 to 1200 USD over 60 seconds.
N += n3
n4 = 60
t4 = np.arange(N, N + n4, 2)  # 80,82,...,138 seconds
base_segment4 = np.linspace(920, 1200, num=len(t4))
# Add some noise around the trend
noise_segment4 = np.random.normal(0, 5, size=len(t4))
segment4 = base_segment4 + noise_segment4

# Combine all segments into a full simulation
times = np.concatenate([t1, t2, t3, t4])
prices = np.concatenate([segment1, segment2, segment3, segment4])
total_points = len(times)

# --- Plot Setup ---
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(times, prices, marker='o', linestyle='-', linewidth=2, markersize=5)
ax.set_title('Stock Price Chart for $BUDML')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Stock Price (USD)')
ax.grid(True)
ax.set_xlim(times[0], times[-1])
ax.set_ylim(min(prices) - 20, max(prices) + 20)

# Create snapshots directory if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
snapshot_dir = script_dir
if not os.path.exists(snapshot_dir):
    os.makedirs(snapshot_dir)

# Save the final image with all data points
current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
#filename = os.path.join(snapshot_dir, f'BUDML_FINAL_{current_date}.png')
filename = os.path.join(snapshot_dir, f'BUDML_FINAL.png')
plt.savefig(filename)
print(f"Saved final image to: {filename}")

# If you still want to show the plot
# plt.show()