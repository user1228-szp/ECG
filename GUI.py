import tkinter as tk

def crear_interfaz(funcion_iniciar, funcion_detener):
    ventana = tk.Tk()
    ventana.title("ECG")
    ventana.geometry("300x150")

    boton_iniciar = tk.Button(ventana, text="Start", command=lambda: [funcion_iniciar(), boton_iniciar.config(state=tk.DISABLED)])
    boton_iniciar.pack(pady=10)

    boton_detener = tk.Button(ventana, text="Stop", command=lambda: [funcion_detener(), boton_iniciar.config(state=tk.NORMAL)])
    boton_detener.pack(pady=10)

    return ventana, boton_iniciar, boton_detener
