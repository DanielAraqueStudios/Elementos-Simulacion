import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp

# =====================================================================
# SYSTEM PARAMETERS (Extracted from main.tex)
T_in = 95.49       # Nominal input torque (N*m) - from T1
T_load = 155.83    # Constant output load torque (N*m) - from T2
r1 = 0.095         # Pitch radius of pinion (m) - from d1/2 (190 mm / 2)
r2 = 0.155         # Pitch radius of gear (m) - from d2/2 (310 mm / 2)

# =====================================================================
# ASSUMED PARAMETERS (As requested)
# =====================================================================
I1 = 0.05          # Inertia of input shaft + pinion (kg*m^2)
I2 = 0.15          # Inertia of output shaft + gear + load (kg*m^2)
km = 5e7           # Gear mesh stiffness (N/m) to simulate micro-vibrations
cm = 1e4           # Gear mesh damping (N*s/m)

# =====================================================================
# DYNAMIC MODEL (2-DOF Torsional System with Mesh Stiffness)
# =====================================================================
def gear_dynamics(t, y, c_fric):
    """
    Differential equations for the gear system.
    y = [theta1, omega1, theta2, omega2]
    c_fric = viscous friction coefficient on shafts
    """
    theta1, omega1, theta2, omega2 = y
    
    # Dynamic Transmission Error (deformation at the gear teeth mesh)
    delta = r1 * theta1 - r2 * theta2
    delta_dot = r1 * omega1 - r2 * omega2
    
    # Gear Mesh Force (Spring-Damper model)
    Fm = km * delta + cm * delta_dot
    
    # Equations of Motion for the input and output shafts
    dtheta1 = omega1
    domega1 = (T_in - Fm * r1 - c_fric * omega1) / I1
    
    dtheta2 = omega2
    domega2 = (Fm * r2 - T_load - c_fric * omega2) / I2
    
    return [dtheta1, domega1, dtheta2, domega2]

# =====================================================================
# SIMULATION SETUP & SOLVER
# =====================================================================
t_span = (0, 0.5)  # Simulate the first 0.5 seconds of startup
t_eval = np.linspace(t_span[0], t_span[1], 2000)
y0 = [0, 0, 0, 0]  # Initial conditions: starting from rest

# Initial solve with default friction
c_fric_init = 0.2
sol = solve_ivp(gear_dynamics, t_span, y0, t_eval=t_eval, args=(c_fric_init,), method='LSODA')

# Convert speeds from rad/s to RPM
omega1_rpm = sol.y[1] * (30 / np.pi)
omega2_rpm = sol.y[3] * (30 / np.pi)

# =====================================================================
# VISUALIZATION & INTERACTIVE SLIDER
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# Plotting speeds
l1, = ax.plot(sol.t, omega1_rpm, label='Input Speed ($\omega_1$)', color='blue')
l2, = ax.plot(sol.t, omega2_rpm, label='Output Speed ($\omega_2$)', color='red')

ax.set_title('Gear Reducer Transient Response & Micro-vibrations')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Rotational Speed (RPM)')
ax.legend()
ax.grid(True)

# Add friction slider
ax_fric = plt.axes([0.2, 0.1, 0.65, 0.03])
fric_slider = Slider(
    ax=ax_fric, 
    label='Friction Loss ($c_{fric}$)', 
    valmin=0.0, 
    valmax=5.0, 
    valinit=c_fric_init,
    color='gray'
)

# Update function for slider
def update(val):
    fric = fric_slider.val
    # Re-solve the system with new friction
    sol_new = solve_ivp(gear_dynamics, t_span, y0, t_eval=t_eval, args=(fric,), method='LSODA')
    
    # Update plot data
    l1.set_ydata(sol_new.y[1] * (30 / np.pi))
    l2.set_ydata(sol_new.y[3] * (30 / np.pi))
    fig.canvas.draw_idle()

fric_slider.on_changed(update)

plt.show()
