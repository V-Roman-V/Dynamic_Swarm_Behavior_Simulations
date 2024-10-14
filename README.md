# Skoltech_Math_for_Engineers_team
Group repository for assignments and project work

**Students:**
1. Roman Voronov (Roman.Voronov@skoltech.ru), Skoltech, 2024
1. Artem Voronov (Artem.Voronov@skoltech.ru), Skoltech, 2024
1. Lev Ladanov (Lev.Ladanov@skoltech.ru), Skoltech, 2024

## Project week 1 simulation
![simulation](<Project_week_1/simulation0.gif>)

### description

This system can be described by the following differential equation:

$$
\dot{x} = A x
$$

where $x$ is a vector representing the positions of points in a plane, with each element $x_i = [X_i, Y_i]$ representing the coordinates of the $i$-th point.

To model the behavior in which the $i$-th agent tends to position itself at the midpoint of the segment formed by the $(i-1)$-th and $(i+1)$-th points, we define the matrix $A$ as follows:

$$
A = 
\begin{bmatrix}
0 &  0 &  0 & \cdots & 0 & 0 & 0 \\
1 & -2 &  1 & \cdots & 0 & 0 & 0 \\
0 &  1 & -2 & \cdots & 0 & 0 & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
0 &  0 &  0 & \cdots & -2 & 1 & 0 \\
0 &  0 &  0 & \cdots & 1 & -2 & 1 \\
0 &  0 &  0 & \cdots & 0 & 0 & 0 \\
\end{bmatrix}
$$

In this matrix, the main diagonal contains the value $-2$, and the first sub-diagonal (just below the main diagonal) and first super-diagonal (just above the main diagonal) contain the value $1$. These entries enforce the rule that each agent moves towards the average position of its two immediate neighbors.

The first and last rows of the matrix $A$ consist of zeros, ensuring that the boundary points remain fixed (i.e., the first and last agents do not move).

### Properties of matrix A:
   - **Tridiagonal** (with entries \(-2\) on the main diagonal, \(1\) on the first sub and superdiagonals).
   - **Sparse** (mostly zeros).
   - **Negative definite** (all eigenvalues are negative).
   - **Real eigenvalues**.

### Finding maximum $\Delta t$:

1. System could be descretize using Euler method:
$$x_{i+1} = x_i + \Delta t \cdot \dot{x} \Leftrightarrow \\
  x_{i+1} = x_i + \Delta t \cdot A x_i \Leftrightarrow \\
  x_{i+1} = (I + \Delta t A) x_i \Leftrightarrow \\
  x_{i+1} = Bx_i \Leftrightarrow \\
  $$


2. System is stable if $\forall |\lambda_i^B| < 1$
3. New eigenvalues equal: $\lambda_i^B = 1 + \Delta t \cdot \lambda_i^A$
4. Since $\forall \lambda_i^A$ are negative, system is stable as long as $1 + \Delta t \cdot \lambda_{min}^A > -1$
5. Eigenvalues of matrix A could be described by formula: $\lambda_i^A = -2 + 2\cos{(\frac{n\pi}{n + 1})} \Rightarrow \lambda_{min}^A \ge -4$
6. $\Delta t \le \frac{-2}{\lambda_{min}^A} \Rightarrow \Delta t \le 0.5$

So the $\Delta t$ should be lower then 0.5 to make system stable.

### Let's test $\Delta t$:

Simultation with $\Delta t = 0.49$:
![alt text](<Project_week_1/simulation_dt49.gif>)

Simultation with $\Delta t = 0.55$:
![alt text](<Project_week_1/simulation_dt55.gif>)

So the estimation of maximum $\Delta t$ is very good.