import numpy as np
import matplotlib.pyplot as plt

d5 = np.array([0.58, 0.83, 1.11])
d50 = np.array([0.58, 0.95, 1.34])
d100 = np.array([0.58, 0.95, 1.35])

n = np.array([1, 2, 3], dtype=np.uint8)

plt.figure()
plt.grid()
plt.plot(n, d5, marker='o', label='MAX_DEPTH = 5')
plt.plot(n, d50, marker='o', label='MAX_DEPTH = 50')
plt.plot(n, d100, marker='o', label='MAX_DEPTH = 100')
plt.xlabel('Number of spheres')
plt.ylabel('Time, s')
plt.title('Render time for 50 samples, C++')
plt.legend()
plt.savefig('plots50_cpp.png')
plt.close()