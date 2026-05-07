# 1)  Import Data 

import csv                          # for data
import matplotlib.pyplot as plt     # for plotting
import numpy as np                  # for sine function

t = [] # column 0
data1 = [] # column 1

filename = "sigA.csv"  

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

# 4a) Signal VS Time Plots
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(t, y,'b')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title("Signal vs Time")

# 4b) FFT Plot
ax2.loglog(frq, abs(Y),'b') # plotting the fft
ax2.set_xlabel('Freq (Hz)')
ax2.set_ylabel('|Y(freq)|')
ax2.set_title("FFT (Frequency Domain)")

plt.tight_layout()
plt.show()
