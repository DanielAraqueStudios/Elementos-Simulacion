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

## 📄 Resumen de Especificaciones Mecánicas (`main.tex`)

El cálculo contenido en el repositorio cubre integralmente:

- **Motorización:** Acoplamiento con motor asíncrono trifásico C.A. de 15 kW operando a 1500 RPM reales.
- **Relación de Transmisión:** Reductor en 1 sola etapa con $i = 1.63$ garantizando una salida estable de $\sim 919$ RPM para la banda transportadora.
- **Materiales Mecánicos:** 
  - *Engranajes:* Acero cementado 20MnCr5.
  - *Ejes:* Acero C45 templado.
  - *Carcasa:* Acero inoxidable X5CrNiMo17-12-2 (AISI 316).
- **Criterios de Fallo:** Verificación por límite de fatiga (Goodman), deformación estática (Von Mises) y fiabilidad rodamientos SKF DIN 625.