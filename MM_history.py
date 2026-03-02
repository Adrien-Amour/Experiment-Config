import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === Load CSV ===
csv_file = 'dc_null_history.csv'

# Load and clean data
df = pd.read_csv(csv_file)  # Use default comma separator
print(df.columns)

df = df.dropna(subset=['H', 'V', 'Date'])
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# === Setup plot ===
fig, ax = plt.subplots()
ax.set_xlim(df['H'].min() - 0.01, df['H'].max() + 0.01)
ax.set_ylim(df['V'].min() - 0.01, df['V'].max() + 0.01)
ax.set_title('Time-Evolving DC Null')
ax.set_xlabel('H')
ax.set_ylabel('V')

# Trail and moving dot
trail, = ax.plot([], [], 'b-', alpha=0.3, lw=2)  # semi-transparent trail
dot, = ax.plot([], [], 'ro', markersize=6)      # red moving dot

# === Animation update function ===
def update(frame):
    x = df['H'].iloc[:frame+1]
    y = df['V'].iloc[:frame+1]
    trail.set_data(x, y)
    dot.set_data([x.iloc[-1]], [y.iloc[-1]])  # <-- wrap in list
    return trail, dot

# === Animate ===
ani = animation.FuncAnimation(
    fig, update, frames=len(df), interval=200, blit=True, repeat=False
)

plt.tight_layout()
plt.show()