import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
N = 5
dt = 0.01  # Time step

x = np.random.random((N, 2))  # Initial random positions of points
A = getA(N, speed_coeff=10)  # Speed coefficient for the system

# Initialize figure and axis for animation
fig, ax = plt.subplots()
scat = ax.scatter(x[:, 0], x[:, 1], s=50)  # Initial scatter plot with marker size
line, = ax.plot([], [], 'r--', lw=2)  # Dashed line between first and last points
traces = [ax.plot([], [], 'b-', lw=1)[0] for _ in range(N)]  # Traces for each point

ax.set_xlim(0, 1)  # Set limits for the x-axis
ax.set_ylim(0, 1)  # Set limits for the y-axis

# To store past positions for traces
trace_data = [np.empty((0, 2)) for _ in range(N)]


# Update function for animation
def update(frame):
    global x  # Ensure we modify the global variable x
    x = x + dx_dt(A, x) * dt
    scat.set_offsets(x)
    
    # Set special properties for the first and last points (red color and larger size)
    colors = ['red'] + ['blue'] * (N - 2) + ['red']
    sizes = [100] + [50] * (N - 2) + [100]
    scat.set_color(colors)
    scat.set_sizes(sizes)
    
    # Update dashed line between first and last points
    line.set_data([x[0, 0], x[-1, 0]], [x[0, 1], x[-1, 1]])
    
    # Update traces for each point (except first and last)
    for i in range(N):
        trace_data[i] = np.vstack([trace_data[i], x[i]])  # Add new position to the trace
        traces[i].set_data(trace_data[i][:, 0], trace_data[i][:, 1])  # Update trace line
    
    return scat, line, *traces

ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=100, blit=True)
plt.show()
