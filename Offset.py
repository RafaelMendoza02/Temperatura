import sys
import board
import busio
import adafruit_max31865 
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.cm import ScalarMappable
from digitalio import DigitalInOut
from gpiozero.pins.pigpio import PiGPIOFactory
import matplotlib.pyplot as plt

# Configuración de pines GPIO
SENSOR_1_CS_PIN = board.D5
SENSOR_2_CS_PIN = board.D6
SENSOR_3_CS_PIN = board.D17

# Intervalo de actualización de la gráfica (en milisegundos)
UPDATE_INTERVAL = 1000

# Rango de temperatura
TEMPERATURE_MIN = -50
TEMPERATURE_MAX = 50

# Configuración de la ventana principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de los sensores
        factory = PiGPIOFactory()
        self.sensor_1 = adafruit_max31865.MAX31865(busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), DigitalInOut(SENSOR_1_CS_PIN))
        self.sensor_2 = adafruit_max31865.MAX31865(busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), DigitalInOut(SENSOR_2_CS_PIN))
        self.sensor_3 = adafruit_max31865.MAX31865(busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), DigitalInOut(SENSOR_3_CS_PIN))

        # Crear la figura y el lienzo de la gráfica
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        # Configuración del diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Configuración del botón de offset
        self.offset_button = QPushButton("Ajustar Offset", self)
        self.offset_button.clicked.connect(self.set_offset)
        layout.addWidget(self.offset_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Configuración del temporizador para actualizar la gráfica
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(UPDATE_INTERVAL)

        # Etiquetas de texto para los valores dentro de las barras
        self.bar_labels = []

        # Crear una barra de colores para la escala de temperatura
        self.colorbar = self.create_colorbar()

        # Variable para almacenar el offset de cada sensor
        self.offsets = [0, 0, 0]

    def set_offset(self):
        # Abrir un cuadro de diálogo para ingresar el valor de offset para cada sensor
        for i, sensor_name in enumerate(['PCA', 'CA1', 'CA2']):
            offset, ok = QInputDialog.getDouble(self, f"Ajustar Offset para {sensor_name}", f"Ingrese el offset para {sensor_name}:")
            if ok:
                operation, ok = self.choose_operation()
                if ok:
                    if operation == "Sumar":
                        self.offsets[i] = offset
                    else:
                        self.offsets[i] = -offset
                    self.update_graph()

    def choose_operation(self):
        # Abrir un cuadro de diálogo para elegir la operación (sumar o restar)
        options = ["Sumar", "Restar"]
        choice, ok = QInputDialog.getItem(self, "Elige una operación", "Operación:", options, 0, False)
        return choice, ok

    def create_colorbar(self):
        # Crear una barra de colores usando ScalarMappable
        norm = plt.Normalize(TEMPERATURE_MIN, TEMPERATURE_MAX)
        cmap = plt.cm.get_cmap('coolwarm')
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        # Crear el colorbar y ajustar su posición
        cbar = self.fig.colorbar(sm, ax=self.ax)
        cbar.ax.set_ylabel('Temperatura (°C)')

        return cbar

    def update_graph(self):
        # Obtener los valores de temperatura de los sensores con los offsets aplicados
        temp_1 = self.sensor_1.temperature + self.offsets[0]
        temp_2 = self.sensor_2.temperature + self.offsets[1]
        temp_3 = self.sensor_3.temperature + self.offsets[2]

        # Actualizar la gráfica con los nuevos valores
        self.ax.clear()
        bar_positions = [0, 1, 2]
        bar_heights = [temp_1, temp_2, temp_3]
        bars = self.ax.barh(bar_positions, bar_heights, tick_label=['PCA', 'CA1', 'CA2'], color=self.colorbar.cmap(self.colorbar.norm(bar_heights)))
        self.ax.tick_params(axis='y', labelsize=40)  # Aumentar el tamaño de letra a 30

        # Actualizar las etiquetas de texto dentro de las barras
        for i, bar in enumerate(bars):
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_y() + bar.get_height() / 2
            label = f"{bar_heights[i]:0.1f} °C"

            if i == len(self.bar_labels) or not self.bar_labels[i]:
                # Si el índice está fuera del rango o la etiqueta no existe, la agregamos
                self.bar_labels.append(self.ax.text(x, y, label, ha='center', va='center', color='black', fontweight='bold', fontsize=40))
            else:
                # Si la etiqueta existe, la actualizamos
                self.bar_labels[i].set_text(label)
                self.bar_labels[i].set_position((x, y))
                self.bar_labels.append(self.ax.text(x, y, label, ha='center', va='center', color='black', fontweight='bold', fontsize=80))

        self.ax.set_xlabel('Temperatura (°C)')
        self.ax.set_ylabel('Sensor')
        self.ax.set_title('Valores de temperatura')
        self.ax.set_xlim(TEMPERATURE_MIN, TEMPERATURE_MAX)

        # Dibujar la gráfica en el lienzo
        self.canvas.draw()

# Crear la aplicación y mostrar la ventana principal
app = QApplication(sys.argv)

window = MainWindow()
window.show()

# Hacer que la ventana se inicie a pantalla completa
window.showFullScreen()

# Ejecutar la aplicación y mostrar la ventana principal
app.exec_()