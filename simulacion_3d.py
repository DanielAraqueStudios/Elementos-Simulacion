import sys
import math
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSlider, QLabel, 
                             QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                             QGroupBox, QGridLayout, QDoubleSpinBox, QGraphicsDropShadowEffect)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QFont, QColor

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print("PyOpenGL is not installed. Please run: pip install PyOpenGL PyOpenGL_accelerate")
    sys.exit(1)

# =====================================================================
# 3D OPENGL WIDGET FOR MECHANISM
# =====================================================================
class MechanismGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theta1 = 0.0
        self.theta2 = 0.0
        self.r1 = 1.9  
        self.r2 = 3.1  
        self.z_zoom = -12.0
        self.x_rot = 20.0
        self.y_rot = 0.0

    def initializeGL(self):
        glClearColor(0.12, 0.12, 0.14, 1.0) # Sleeker dark background
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        light_pos = [5.0, 5.0, 10.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h > 0 else 1
        gluPerspective(45.0, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, self.z_zoom)
        glRotatef(self.x_rot, 1.0, 0.0, 0.0)
        glRotatef(self.y_rot, 0.0, 1.0, 0.0)
        
        # Pinion Gear
        glPushMatrix()
        glTranslatef(-self.r1, 0.0, 0.0)
        glRotatef(math.degrees(self.theta1), 0.0, 0.0, 1.0)
        glColor3f(0.0, 0.47, 0.83) # Modern Qt Blue
        self.draw_gear(self.r1, 19, 0.5)
        glPopMatrix()

        # Corona Gear
        glPushMatrix()
        glTranslatef(self.r2, 0.0, 0.0)
        glRotatef(math.degrees(self.theta2), 0.0, 0.0, 1.0)
        glColor3f(0.85, 0.33, 0.1) # Modern Accent Orange
        self.draw_gear(self.r2, 31, 0.5)
        glPopMatrix()

    def draw_gear(self, radius, teeth, thickness):
        slices = teeth * 2
        half_z = thickness / 2.0
        glBegin(GL_QUADS)
        for i in range(slices):
            angle1 = i * 2.0 * math.pi / slices
            angle2 = (i + 1) * 2.0 * math.pi / slices
            r_outer1 = radius * (1.1 if i % 2 == 0 else 1.0)
            r_outer2 = radius * (1.0 if i % 2 == 0 else 1.1)
            x1, y1 = math.cos(angle1) * r_outer1, math.sin(angle1) * r_outer1
            x2, y2 = math.cos(angle2) * r_outer2, math.sin(angle2) * r_outer2
            
            glNormal3f(0.0, 0.0, 1.0)
            glVertex3f(0.0, 0.0, half_z)
            glVertex3f(x1, y1, half_z)
            glVertex3f(x2, y2, half_z)
            glVertex3f(0.0, 0.0, half_z)
            
            glNormal3f(0.0, 0.0, -1.0)
            glVertex3f(0.0, 0.0, -half_z)
            glVertex3f(x2, y2, -half_z)
            glVertex3f(x1, y1, -half_z)
            glVertex3f(0.0, 0.0, -half_z)
            
            nx, ny = x1 + x2, y1 + y2
            ln = math.sqrt(nx**2 + ny**2)
            if ln > 0: glNormal3f(nx/ln, ny/ln, 0.0)
            glVertex3f(x1, y1, half_z)
            glVertex3f(x1, y1, -half_z)
            glVertex3f(x2, y2, -half_z)
            glVertex3f(x2, y2, half_z)
        glEnd()

# =====================================================================
# MAIN APPLICATION WINDOW
# =====================================================================
class MechanismSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProGear Dynamics - 3D Mechanisms")
        self.resize(1200, 750)
        self.apply_dark_theme()

        # Physics Parameters
        self.I1 = 0.05
        self.I2 = 0.15
        self.ratio = 31.0 / 19.0
        self.I_eq = self.I1 + self.I2 / (self.ratio**2)
        
        self.T_in = 150.0
        self.T_load = 50.0
        self.c_fric = 0.5
        self.target_speed_rpm = 1500.0 
        
        self.omega1 = 0.0
        self.theta1 = 0.0
        self.omega2 = 0.0
        self.theta2 = 0.0
        
        self.running = False
        
        self.init_ui()
        
        self.dt = 0.016 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_labels)

    def apply_dark_theme(self):
        dark_style = """
        QMainWindow { background-color: #121214; }
        QWidget {
            background-color: #121214;
            color: #E0E0E0;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        }
        QGroupBox {
            background-color: #1E1E22;
            border: 1px solid #2B2D31;
            border-radius: 8px;
            margin-top: 1.5em;
            padding: 15px;
        }
        QGroupBox::title {
            color: #61AFEF;
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QLabel { font-size: 13px; background: transparent; }
        
        /* Modern SpinBox Control */
        QDoubleSpinBox {
            background-color: #2D2D30;
            color: #5CE6CD;
            border: 1px solid #3E3E42;
            border-radius: 4px;
            padding: 4px;
            font-family: 'Consolas', monospace;
            font-weight: bold;
        }
        QDoubleSpinBox:focus { border: 1px solid #61AFEF; }
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0px; } /* Hide arrows for a clean look */
        
        /* Interactive Buttons */
        QPushButton {
            background-color: #0E639C;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        QPushButton:hover { background-color: #1177BB; }
        QPushButton:pressed { background-color: #0D588C; }
        QPushButton#resetBtn { background-color: #D32F2F; border: 1px solid #B71C1C; }
        QPushButton#resetBtn:hover { background-color: #F44336; }
        
        /* Sliders */
        QSlider::groove:horizontal {
            border: none;
            height: 6px;
            background: #2B2D31;
            border-radius: 3px;
        }
        QSlider::sub-page:horizontal {
            background: #0E639C;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #FFFFFF;
            border: 2px solid #0E639C;
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #5CE6CD;
            border-color: #5CE6CD;
        }
        """
        self.setStyleSheet(dark_style)

    def create_param_control(self, layout, row, title, val, min_v, max_v, step, unit, callback):
        # Label with HTML for proper subscript rendering
        lbl = QLabel(title)
        
        # Double Spin Box for Precise Input
        spin = QDoubleSpinBox()
        spin.setRange(min_v, max_v)
        spin.setValue(val)
        spin.setSingleStep(step)
        spin.setSuffix(f" {unit}")
        spin.setFixedWidth(110)
        
        # Slider for visual UX
        slider = QSlider(Qt.Orientation.Horizontal)
        # Scale for float precision in slider
        scale = 10 if step < 1 else 1
        slider.setRange(int(min_v * scale), int(max_v * scale))
        slider.setValue(int(val * scale))
        
        # Syncing Logic
        def on_slider(v):
            spin.blockSignals(True)
            spin.setValue(v / scale)
            spin.blockSignals(False)
            callback(v / scale)
            
        def on_spin(v):
            slider.blockSignals(True)
            slider.setValue(int(v * scale))
            slider.blockSignals(False)
            callback(v)

        slider.valueChanged.connect(on_slider)
        spin.valueChanged.connect(on_spin)

        layout.addWidget(lbl, row, 0, 1, 2)
        layout.addWidget(slider, row+1, 0)
        layout.addWidget(spin, row+1, 1)

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)
        
        # Left: 3D Visualization
        self.gl_widget = MechanismGLWidget()
        
        main_layout.addWidget(self.gl_widget, stretch=2)
        
        # Right: Control Panel
        control_panel = QWidget()
        control_panel.setFixedWidth(380)
        vbox = QVBoxLayout(control_panel)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(15)

        # Title
        app_title = QLabel("⚙️ Mechanism Control System")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        app_title.setStyleSheet("color: #FFFFFF; padding-bottom: 5px;")
        vbox.addWidget(app_title)

        # PARAMETERS GROUP
        params_group = QGroupBox("Dynamic Constraints")
        params_layout = QGridLayout()
        params_layout.setVerticalSpacing(15)
        
        self.create_param_control(params_layout, 0, "Motor Torque (T<sub>in</sub>)", self.T_in, 0, 300, 1, "N·m", self.on_tin_change)
        self.create_param_control(params_layout, 2, "Conveyor Load (T<sub>load</sub>)", self.T_load, 0, 300, 1, "N·m", self.on_tload_change)
        self.create_param_control(params_layout, 4, "Target Speed (ω<sub>target</sub>)", self.target_speed_rpm, 0, 2000, 10, "RPM", self.on_speed_slider_change)
        self.create_param_control(params_layout, 6, "System Friction (c<sub>fric</sub>)", self.c_fric, 0.0, 10.0, 0.1, "N·s/m", self.on_fric_change)

        params_group.setLayout(params_layout)
        vbox.addWidget(params_group)

        # TELEMETRY GROUP
        data_group = QGroupBox("Live Kinematic Telemetry")
        data_layout = QGridLayout()
        data_layout.setSpacing(10)
        
        self.lbl_speed1 = QLabel("0.0 RPM")
        self.lbl_speed2 = QLabel("0.0 RPM")
        self.lbl_kinetic = QLabel("0.0 J")
        
        font_lbl = QFont("Segoe UI", 12)
        font_data = QFont("Consolas", 14, QFont.Weight.Bold)
        
        labels = [("Input Speed:", self.lbl_speed1), 
                  ("Output Speed:", self.lbl_speed2), 
                  ("Kinetic Energy:", self.lbl_kinetic)]
                  
        for row, (text, val_lbl) in enumerate(labels):
            title_lbl = QLabel(text)
            title_lbl.setFont(font_lbl)
            title_lbl.setStyleSheet("color: #8B8D91;")
            
            val_lbl.setFont(font_data)
            val_lbl.setStyleSheet("color: #5CE6CD; text-align: right;")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
            data_layout.addWidget(title_lbl, row, 0)
            data_layout.addWidget(val_lbl, row, 1)
            
        data_group.setLayout(data_layout)
        vbox.addWidget(data_group)

        # BUTTONS
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("▶ Start")
        self.btn_start.clicked.connect(self.toggle_simulation)
        
        self.btn_reset = QPushButton("↺ Reset")
        self.btn_reset.setObjectName("resetBtn") # For specific CSS
        self.btn_reset.clicked.connect(self.reset_simulation)
        
        btn_layout.addWidget(self.btn_start, stretch=2)
        btn_layout.addWidget(self.btn_reset, stretch=1)
        vbox.addLayout(btn_layout)
        
        vbox.addStretch()
        main_layout.addWidget(control_panel)
        self.setCentralWidget(central_widget)

    # --- Callbacks ---
    def on_tin_change(self, val): self.T_in = float(val)
    def on_tload_change(self, val): self.T_load = float(val)
    def on_speed_slider_change(self, val): self.target_speed_rpm = float(val)
    def on_fric_change(self, val): self.c_fric = float(val)

    def toggle_simulation(self):
        if self.running:
            self.timer.stop()
            self.telemetry_timer.stop()
            self.btn_start.setText("▶ Start")
            self.btn_start.setStyleSheet("background-color: #0E639C;")
            self.running = False
        else:
            self.timer.start(int(self.dt * 1000))
            self.telemetry_timer.start(200)
            self.btn_start.setText("⏸ Pause")
            self.btn_start.setStyleSheet("background-color: #FF9800;") # Warning Orange when running
            self.running = True

    def reset_simulation(self):
        self.omega1 = self.theta1 = self.omega2 = self.theta2 = 0.0
        self.gl_widget.theta1 = self.gl_widget.theta2 = 0.0
        self.gl_widget.update()
        self.update_labels()

    def update_simulation(self):
        T_load_eq = self.T_load / self.ratio
        c_eq = self.c_fric + (self.c_fric / (self.ratio**2))
        target_omega = self.target_speed_rpm * math.pi / 30.0
        err = target_omega - self.omega1
        
        applied_torque = 150.0 * err 
        if applied_torque > 0:
            applied_torque = min(applied_torque, self.T_in)
        else:
            applied_torque = max(applied_torque, -self.T_in)
        
        actual_load = T_load_eq
        if self.omega1 <= 0.01 and applied_torque < T_load_eq:
            actual_load = applied_torque
            
        alpha1 = (applied_torque - actual_load - c_eq * self.omega1) / self.I_eq
        
        self.omega1 += alpha1 * self.dt
        if self.omega1 < 0 and self.target_speed_rpm >= 0:
            self.omega1 = 0.0
            
        self.theta1 += self.omega1 * self.dt
        self.omega2 = self.omega1 / self.ratio
        self.theta2 = -(self.theta1 / self.ratio)
        
        self.gl_widget.theta1 = self.theta1
        self.gl_widget.theta2 = self.theta2
        self.gl_widget.update()

    def update_labels(self):
        rpm1 = self.omega1 * 30 / math.pi
        rpm2 = self.omega2 * 30 / math.pi
        ke = 0.5 * self.I1 * (self.omega1**2) + 0.5 * self.I2 * (self.omega2**2)
        
        self.lbl_speed1.setText(f"{rpm1:06.1f} RPM")
        self.lbl_speed2.setText(f"{rpm2:06.1f} RPM")
        self.lbl_kinetic.setText(f"{ke:07.1f} J")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MechanismSimulator()
    window.show()
    sys.exit(app.exec())