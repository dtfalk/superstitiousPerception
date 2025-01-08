import numpy as np
import matplotlib.pyplot as plt

# List of sigma values to test
sigma_values = [1, 2, 3, 4, 5]  # You can change these values to whatever you'd like to test

# Distance range from 0 to 25
distances = np.linspace(0, 25, 100)

plt.figure(figsize=(10, 5))

# Plotting each sigma value
for sigma in sigma_values:
    weights = np.exp(-distances**2 / (2 * sigma**2))
    plt.plot(distances, weights, label=f'Sigma = {sigma}')

plt.xlabel('Distance (Pixels)')
plt.ylabel('Weight (Normalized)')
plt.title('Gaussian Weighting for Different Sigma Values')
plt.legend()
plt.grid(True)
plt.show()
