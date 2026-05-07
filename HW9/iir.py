import csv                          # for data
import matplotlib.pyplot as plt     # for plotting
import numpy as np                  # for sine function

t = [] # column 0
data1 = [] # column 1

filename = "sigD.csv"  

with open(filename, "r") as f:
    # open the csv file
    reader = csv.reader(f)

    for row in reader:
        # read the rows 1 one by one
        t.append(float(row[0])) # leftmost column
        data1.append(float(row[1])) # second column

# convert to numpy arrays
t = np.array(t)
y = np.array(data1)

# 3) Compute Sample Rate
total_time = t[-1] - t[0] 
n = len(y)              

Fs  = n/total_time

# 4 ) FFT
k = np.arange(n)
T = n/Fs

frq = k/T # two sides frequency range

frq = frq[range(int(n/2))] # one side frequency range
Y = np.fft.fft(y)/n # fft computing and normalization
Y = Y[range(int(n/2))]

# 5) Moving Average filter

def iir_filter(signal, A, B):
    y = []
    y_prev = 0

    for i in range(len(signal)):

        y_new = A * y_prev + B * signal[i]
        y.append(y_new)

        y_prev = y_new

    return np.array(y)

A = 0.85
B = 0.15

y_filtered = iir_filter(y, A, B)

Y_filtered = np.fft.fft(y_filtered) / n
Y_filtered = Y_filtered[range(int(n/2))]

fig, (ax1, ax2) = plt.subplots(2, 1)

# 5a) Signal VS Time Plots
ax1.plot(t, y, 'k', label='Unfiltered')            
ax1.plot(t, y_filtered, 'r', label='Filtered') 

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title(f'IIR Filter VS. Time  (A = {A}, B = {B})')
ax1.legend()

# 5b) FFT Plot
ax2.plot(frq, abs(Y), 'k', label='Unfiltered FFT')
ax2.plot(frq, abs(Y_filtered), 'r', label='Filtered FFT')

ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('|Y(f)|')
ax2.set_title('FFT Comparison')
ax2.legend()

plt.tight_layout()
plt.show()