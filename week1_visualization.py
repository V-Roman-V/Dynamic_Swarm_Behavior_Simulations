import os
from modules.animation import SimulationAnimation
from Project_week_1.system import System

def get_next_filename(folder='',prefix='simulation', ext='.gif'):
    num = len([file for file in os.listdir(folder) if file.lower().endswith(ext)])
    return os.path.join(folder,f'{prefix}{num}{ext}')

def main():
    # Configuration
    N = 8
    dt = 0.15  # max is 0.5
    
    # Initialize the system
    system = System(N)
    animation = SimulationAnimation(system, dt)

    ani = animation.run_animation(frames=100, interval=100)
    ani.save(get_next_filename(folder='Project_week_1'), writer='pillow', fps=10)

if __name__ == "__main__":
    main()
