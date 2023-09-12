import numpy as np


def jeffress_model(left_signal, right_signal, max_delay, fs):
    # Calculate the possible delay in samples
    delay_samples = round(max_delay * fs)

    # Initialize the activation array
    activation = np.zeros(2 * delay_samples + 1)

    # Loop through each possible ITD
    for d in range(-delay_samples, delay_samples + 1):
        if d < 0:
            shifted_left = np.concatenate((np.zeros(abs(d)), left_signal[:d]))
            activation[d + delay_samples] = np.sum(shifted_left * right_signal)
        elif d > 0:
            shifted_right = np.concatenate((np.zeros(d), right_signal[:-d]))
            activation[d + delay_samples] = np.sum(left_signal * shifted_right)
        else:
            activation[d + delay_samples] = np.sum(left_signal * right_signal)

    # Find the delay with maximum activation
    max_index = np.argmax(activation)
    itd = (max_index - delay_samples) / fs

    return itd, activation


# Test the function
left_signal = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
right_signal = np.array([0.0, 0.1, 0.2, 0.3, 0.4])
max_delay = 0.5  # in seconds
fs = 10  # sampling frequency in Hz

itd, activation = jeffress_model(left_signal, right_signal, max_delay, fs)
print(f"Computed ITD: {itd} seconds")
print(f"Activation levels: {activation}")
