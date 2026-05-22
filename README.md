# Diseño y Simulación de Conjunto Reductor de Engranajes ⚙️

Este repositorio contiene el desarrollo integral de un conjunto reductor de engranajes cilíndricos rectos de una etapa, diseñado específicamente para un sistema de banda transportadora industrial. 

El proyecto consta de dos núcleos principales:
1. **Memoria Técnica y Diseño (LaTeX):** Documentación completa y estructurada bajo formato APA 7ma edición, detallando el diseño analítico, cinemático y geométrico, así como el modelado en SolidWorks.
2. **Simulación 3D e Interfaz Interactiva (Python):** Aplicación de escritorio que renderiza en tiempo real el comportamiento del sistema mediante OpenGL, integrando un motor físico para simular inercias, reducción de velocidad y multiplicación de torque.

---

## 👥 Autores
**Ingeniería Mecatrónica - Universidad Militar Nueva Granada**
* Miguel A. Rojas
* Sebastián A. Rodríguez
* David A. Rodriguez
* Jose A. Rincon
* Daniel García Araque

---

## 🛠️ Stack Tecnológico

* **Documentación:** LaTeX (PDFLaTeX).
* **Modelado CAD:** SolidWorks (Exportado para representación esquemática).
* **Simulación en Tiempo Real / Software:** 
  * Python 3.13
  * `PyQt6` (Frontend y ventanas de Interfaz de Usuario)
  * `PyOpenGL` (Renderizado Gráfico 3D mediante aceleración de hardware)
  * `SciPy` & `NumPy` (Cálculo de ecuaciones diferenciales y matrices para la física)

---

## 🚀 Guía de Uso del Simulador 3D v2

### 1. Requisitos previos
Asegúrate de contar con Python 3.10 o superior instalado en tu sistema. Luego, instala las librerías científicas y gráficas necesarias de forma global o en un entorno virtual:

```powershell
pip install PyQt6 PyOpenGL PyOpenGL_accelerate numpy scipy
```

### 2. Ejecución
Para arrancar el motor físico 3D interactivo en su última versión, sitúate en la raíz del proyecto y ejecuta:

```powershell
python simulacion_3d_v2.py
```

### 3. Interacción UI y Nuevas Características v2
* **Control PI (Proporcional-Integral):** El motor ahora simula una aceleración y torque realista que reacciona a la inercia del sistema y la carga de fricción (`c_fric`) y momento resistente (`T_load`).
* **Sincronización Cinemática de Engranes:** Corrección del *pitch* y offset de fase. La cinemática de los dientes ahora interactúa físicamente a la perfección sin sobrelaparse (manteniendo espaciado `addendum` y `dedendum` real).
* **Física en Tiempo Real:** El cálculo de Euler fue actualizado para basarse en reloj real (`time.perf_counter`) garantizando sincronía temporal gráfica sin importar el lag o bloqueos UI.
* **Osciloscopio / Plotter en Tiempo Real:** Interfaz QPainter customizada para graficar con curvas precisas la velocidad de Entrada vs. Salida en todo instante de aceleración y desaceleración.
* **Estilizado Avanzado UI:** Tema oscuro con botones de estados dinámicos, sombras en la vista renderizada y panel de recolección de métricas.

---

## 📄 Resumen del Diseño y Cálculos Mecánicos (`main.tex`)

El cálculo analítico documentado cubre integralmente el diseño del sistema reductor para servicio continuo:

### 1. Motorización y Cinemática
- **Transmisión:** Reductor de 1 etapa mediante engranajes cilíndricos rectos (Módulo $m=10$ mm).
- **Motor:** Asíncrono trifásico C.A. de jaula de ardilla, **15 kW** operando a **1500 RPM** nominales (Servicio S1 continuo).
- **Relación de Transmisión ($i$):** Piñón conductor ($Z_1 = 19$) a Rueda conducida ($Z_2 = 31$). Resultando en $i \approx 1.632$.
- **Geometría de Engranes:**
  - Radio primitivo piñón ($r_1$): $95$ mm.
  - Radio primitivo rueda ($r_2$): $155$ mm.
  - Distancia interaxial ($c = r_1 + r_2$): $250$ mm.
- **Salida:** Velocidad nominal en el eje conducido de **919.1 RPM** ($\approx 96.24$ rad/s) con un torque neto entregado de **155.9 N·m** ($155,900$ N·mm).

### 2. Análisis Dinámico y Fuerzas de Engrane
Considerando un ángulo de presión estándar de $\phi = 20^\circ$, las cargas resultantes transmitidas en los dientes para el diseño del eje fueron:
- Fuerza Tangencial ($W_t = T / r_2$): **1005.8 N**
- Fuerza Radial separadora ($W_r = W_t \cdot \tan 20^\circ$): **366.0 N**
- Fuerza Resultante Normal ($W_n = W_t / \cos 20^\circ$): **1070.3 N**
*(Las cargas axiales $W_a$ son nulas por tratarse de engranajes cilíndricos de diente recto).*

### 3. Diseño del Eje y Fatiga
El eje se evaluó bajo un análisis iterativo para flexión y torsión combinadas, tomando componentes de fatiga para carga alternante (flexión rotatoria) y par constante:
- **Material de Eje:** Acero AISI 4340 / 42CrMo4 (Acero de alta resistencia a la tracción; Límite Fluencia $S_y = 862$ MPa, Límite de fatiga corregido por factores de Marín $S_e = 258$ MPa).
- **Metodología de Falla:** Teoría de falla por fatiga **ASME-Elliptic** y criterios de Shigley.
- **Dimensionamiento Analítico vs. Pragmático:**
  - El diámetro analítico mínimo contra falla combinada en el escalón crítico arrojó apenas **22.7 mm**.
  - Sin embargo, para cumplir con el acoplamiento a ejes comerciales, absorción de cargas de impacto extremo (factor de servicio industrial), y estandarización del montaje directo con los **Rodamientos Radiales Rígidos (SKF 635-20312)**, se aplicó un factor de robustez $\Phi_d = 60$.
  - El diámetro principal comercial adoptado se fijó en **90 mm**, lo que hiperdimensiona la confiabilidad entregando un **Factor de Seguridad Final ($N_{\text{real}}$) de 14.3**.

### 4. CAD, Ajustes y Validación FEM (Elementos Finitos)
- **Ajustes y Tolerancias:** 
  - Se confirmó en SolidWorks un juego de cabeza estándar de **0.5 mm** ($c^* = 0.25m$) entre flancos (0% de interferencia volumétrica), permitiendo el flujo de lubricante (aceite térmico).
  - Los rodamientos (SKF 635-20312) se alojaron con un ajuste de apriete en alojamiento / eje de **H7/k6 - k6/h6** garantizando unión a interferencia para soportar la carga radial continua y mitigar del deslizamiento anular.
- **Análisis de Esfuerzos FEM:** El ensamble completo y el eje se sometieron a Elementos Finitos (SolidWorks Simulation) validando concentraciones de esfuerzos en cambios de sección y ranuras de anillos *Circlip DIN 471*, mostrando deformaciones de Von Mises que coinciden y respetan los límites elásticos de fluencia del material seleccionado.
- **Materiales del Sistema Final:**
  - *Engranajes y Piñones:* Acero cementado 20MnCr5 (dureza y resistencia al desgaste en los flancos).
  - *Ejes:* Acero 4340/42CrMo4 templado.
  - *Carcasa estructural:* Acero inoxidable X5CrNiMo17-12-2 (AISI 316) blindado contra ambientes corrosivos, sellado con tapetas ciegas/pasantes y sellos de caucho O-Ring para retención de aceite de lubricación.