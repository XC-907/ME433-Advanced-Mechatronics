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

k = np.arange(n)
T = n / Fs

frq = k / T
frq = frq[range(int(n/2))] # one side frequency range

# Import coefficients
h = np.array([
    0.000000000000000000,
    0.000051896829378561,
    0.000000000000000000,
    -0.000572714021280865,
    0.000000000000000001,
    0.002074355812247745,
    -0.000000000000000003,
    -0.005431952967813019,
    0.000000000000000005,
    0.012025581223298653,
    -0.000000000000000008,
    -0.024089253454506038,
    0.000000000000000012,
    0.046316296574514276,
    -0.000000000000000016,
    -0.094755853941549451,
    0.000000000000000019,
    0.314370394948385368,
    0.500022497994649484,
    0.314370394948385368,
    0.000000000000000019,
    -0.094755853941549464,
    -0.000000000000000016,
    0.046316296574514290,
    0.000000000000000012,
    -0.024089253454506038,
    -0.000000000000000008,
    0.012025581223298660,
    0.000000000000000005,
    -0.005431952967813017,
    -0.000000000000000003,
    0.002074355812247745,
    0.000000000000000001,
    -0.000572714021280865,
    0.000000000000000000,
    0.000051896829378561,
    0.000000000000000000
])

def apply_fir(signal, h):

    N = len(h)
    y_out = []

    for i in range(len(signal)):

        acc = 0

        for k in range(N):

            if i - k >= 0:
                acc += h[k] * signal[i - k]

        y_out.append(acc)

    return np.array(y_out)


y_filtered = apply_fir(y, h)

Y = np.fft.fft(y) / n
Yf = np.fft.fft(y_filtered) / n

Y = Y[:n // 2]
Yf = Yf[:n // 2]


# 7a) Signal VS Time Plots
fig, (ax1, ax2) = plt.subplots(2, 1)

# TIME DOMAIN
ax1.plot(t, y, 'k', label='Original')
ax1.plot(t, y_filtered, 'r', label='FIR Filtered')

ax1.set_title('FIR Filter (Low-Pass, 37 Coeffs., Cut off at 100 Hz, & 50 Hz Bandwidth) ')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.legend()

# 7b) FFT Plot
ax2.plot(frq, abs(Y), 'k', label='Original FFT')
ax2.plot(frq, abs(Yf), 'r', label='Filtered FFT')

ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('|Y(f)|')
ax2.set_title('FFT Comparison')
ax2.legend()

plt.tight_layout()
plt.show()