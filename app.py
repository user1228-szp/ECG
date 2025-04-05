import time
import csv
from datetime import datetime
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
import threading
from gui_ecg import crear_interfaz

SAMPLING_TIME = 0.01
Duration = 30
WINDOW_SIZE = 500

data = deque([0.0]*WINDOW_SIZE, maxlen=WINDOW_SIZE)
start = False
start_time = 0
file = None
writer = None

########config. sensor###########
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
canal_ecg = AnalogIn(ads, ADS1115.P0)


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
        voltaje = canal_ecg.voltage
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

##########app############
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
