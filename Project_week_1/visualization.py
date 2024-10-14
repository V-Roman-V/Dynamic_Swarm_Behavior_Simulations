import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Define the system matrix A
def getA(N, speed_coeff):
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = -2
        if i > 0:
            A[i,i-1] = 1
        if i < N-1:
            A[i,i+1] = 1
    A[0] = 0
    A[-1] = 0
    A *= speed_coeff
    return A

# Define the derivative function dx/dt
def dx_dt(A, x):
    return np.dot(A,x)

# Parameters for the system
N = 8
dt = 0.01

x = np.random.random((N, 2))
x[0,0] = x[0,0]/2
x[-1,0] = x[-1,0]/2 + 0.5
A = getA(N, speed_coeff=10)

final_poses = np.asarray([x[0] + (i+1)/(N-1)*(x[-1] - x[0]) for i in range(N-2)])

# Initialize figure and axis for animation
fig, ax = plt.subplots()

size = 100
colors = ['yellow'] + ['lightgreen'] * (N - 2) + ['yellow']
sizes = [2*size] + [size] * (N - 2) + [2*size]

ax.plot([x[0, 0], x[-1, 0]], [x[0, 1], x[-1, 1]], 'r--', lw=2, zorder=0)
ax.scatter(final_poses[:,0],final_poses[:,1], color='k', s=size/4, alpha=0.5, zorder=1)
scat = ax.scatter(x[:, 0], x[:, 1], color=colors, s=sizes, zorder=2)
traces = [ax.plot([], [], 'b-', lw=1, zorder=1)[0] for _ in range(N)]

ax.set_title(f"Simulation Time: 0.00 seconds")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
fig.tight_layout()

trace_data = [np.empty((0, 2)) for _ in range(N)]
text_labels = [ax.text(x[i, 0], x[i, 1], str(i), fontsize=12, ha='center', va='center', zorder=3) for i in range(N)]

# Update function for animation
def update(frame):
    global x
    x = x + dx_dt(A, x) * dt
    scat.set_offsets(x)

    for i in range(N):
        # cur_trace = traces[i].get_data()
        trace_data[i] = np.vstack([trace_data[i], x[i]])
        traces[i].set_data(trace_data[i][:, 0], trace_data[i][:, 1])
    
    for i, text in enumerate(text_labels):
        text.set_position((x[i, 0], x[i, 1]))

    ax.set_title(f"Simulation Time: {frame * dt:.2f} seconds")
    return scat, *text_labels, *traces

ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=100, blit=True)

num = len([file for file in os.listdir('.') if file.lower().endswith('.gif')])
ani.save(f'simulation{num}.gif', writer='pillow', fps=10)
