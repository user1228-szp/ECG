from scipy.fftpack import fft, ifft
import scipy.signal
from scipy.signal import butter,lfilter,freqz
import numpy as np
import matplotlib.pyplot as plt 

class SignalProcessing:
    def __init__(self, fs):
        self.fs = fs

    def butter_lowpass(self, cutoff, fs, order=5):
        return scipy.signal.butter(order, cutoff, fs=fs, btype='low', analog=False)

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = scipy.signal.lfilter(b, a, data)
        return y

    def power_spectrum(self, y_signal, fs, time):
        t = np.arange(-time, time, 1/fs)
        L = len(t)
        n = 2^int(np.ceil(np.log2(L)))
        Y = np.fft.fft(y_signal, n)
        f = fs * (np.arange(n//2 +1)) / n
        P = np.abs(Y/n)
        frec = f
        Power = P[1:n / 2+1]
        
        plt.figure()
        plt.plot(frec, Power)
        plt.xlabel('Frecuencia')
        plt.ylabel('Potencia espectral')
        plt.title('Espectro de potencia')
        plt.show()

    def image_to_array(self, imagen):
        size = (64, 64)
        fig = plt.figure(figsize=(size[1]/100, size[0]/100))
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        plt.specgram(np.array(imagen).flatten(), Fs=self.fs, cmap="gray")

        fig.canvas.draw()
        arr = np.array(fig.canvas.renderer.buffer_rgba())
        gray_arr = np.dot(arr[..., :3], [0.2989, 0.5870, 0.1140])

        # Redimensiona el arreglo al tamaño deseado
        resized_arr = np.resize(gray_arr, size)
        plt.close(fig)
        # Retorna el arreglo redimensionado
        return resized_arr