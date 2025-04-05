import time
import csv
from datetime import datetime
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import smbus
import threading
from GUI import crear_interfaz  # Aquí importa la interfaz gráfica

SAMPLING_TIME = 0.01 
Duration = 30  
WINDOW_SIZE = 500  

data = deque([0.0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
start = False  
start_time = 0 
file = None  
writer = None

########## Configuración del sensor ##########
bus = smbus.SMBus(1)

ADS1115_ADDRESS = 0x48
ADS1115_CONFIG_REGISTER = 0x01
ADS1115_CONVERSION_REGISTER = 0x00

GAIN = 1  # Ganancia
SAMPLES_PER_SECOND = 860  # Tasa de muestreo en muestras por segundo

# Lectura de un solo canal del ADS1115
def read_adc(channel):
    config = 0xC000 + (GAIN << 9)  # Configuración para 16 bits y ganancia
    config |= (0x8000 if channel == 0 else 0x0000)  # Selección de canal

    bus.write_i2c_block_data(ADS1115_ADDRESS, ADS1115_CONFIG_REGISTER, [(config >> 8) & 0xFF, config & 0xFF])
    time.sleep(0.1)  # Tiempo de espera para la conversión
    data = bus.read_i2c_block_data(ADS1115_ADDRESS, ADS1115_CONVERSION_REGISTER, 2)
    return (data[0] << 8) + data[1]

# Función para comenzar la grabación de los datos
def recording():
    global file, writer, start_time
    name = f"ecg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file = open(name, "w", newline="")  
    writer = csv.writer(file)
    writer.writerow(["T", "V"]) 
    start_time = time.time()  

def end_record():
    global file, start
    if file:
        file.close() 
    start = False 
    print("Grabación finalizada.")

def update(frame):
    global start_time
    if start:
        voltaje = read_adc(0) * 0.0001875  
        tiempo_actual = time.time() - start_time 
        data.append(voltaje)  
        writer.writerow([tiempo_actual, voltaje]) 
        line.set_ydata(data) 
        if tiempo_actual >= Duration:  
            end_record()
    return line, 

def start_rec():
    global start
    recording()  
    start = True
    print("Adquisición iniciada.")

def finish_rec():
    end_record()

########## Interfaz gráfica ############
if __name__ == "__main__":
    ventana, boton_iniciar, boton_detener = crear_interfaz(start_rec, finish_rec)

    fig, ax = plt.subplots()
    line, = ax.plot(range(WINDOW_SIZE), data)
    ax.set_ylim(0, 3.3)  
    ax.set_title("ECG")
    ax.set_xlabel("Muestras")
    ax.set_ylabel("Voltaje (V)")
    ani = animation.FuncAnimation(fig, update, interval=SAMPLING_TIME*1000)
    threading.Thread(target=ventana.mainloop).start()
    plt.show()
