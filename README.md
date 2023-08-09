Este proyecto se basa en el registro de temperatura de 3 camaras frigorificas 
lo que necesitaremos sera 3 sensores pt100 o pt1000 RTD platinum

Usaremos lo que son modulos adafruit MAX31865

tendremos que instalar los paquetes o librerias para que el programa funcione correctamente:

PyQt5: Biblioteca para la creación de interfaces gráficas.
pip install PyQt5

matplotlib: Biblioteca para crear gráficos y visualizaciones.
pip install matplotlib

adafruit-blinka: Biblioteca para trabajar con hardware de Adafruit en placas Raspberry Pi y otras placas basadas en Linux.
pip install adafruit-blinka

adafruit-circuitpython-max31865: Biblioteca para trabajar con el módulo MAX31865 y sensores de temperatura RTD.
pip install adafruit-circuitpython-max31865

gpiozero: Biblioteca para controlar pines GPIO en la Raspberry Pi.
pip install gpiozero

Tambien tendras que instalar la extension de Python en el visual studio Code para que puedas ejecutar el programa
acuerdate que si el programa no se ejecuta en una raspberry pi mandara un error el cual no detectara los pines GPIO
