import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(filepath, sequence_length=50, test_size=0.1, random_state=42):
    """
    Preprocess the 'Close' column for LSTM and split into train/test sets.

    Args:
        filepath (str): Path to the CSV file.
        sequence_length (int): Length of input sequences for LSTM.
        test_size (float): Fraction of the data to use as the test set.
        random_state (int): Random seed for reproducibility.

    Returns:
        X_train (np.array): Training input sequences.
        X_test (np.array): Test input sequences.
        y_train (np.array): Training target values.
        y_test (np.array): Test target values.
    """
    # Load the data
    data = pd.read_csv(filepath)

    # Extract the 'Close' column
    close_prices = data['Close'].values.reshape(-1, 1)  # Shape: (num_samples, 1)

    # Normalize the 'Close' column
    scaler = MinMaxScaler()
    close_scaled = scaler.fit_transform(close_prices)  # Shape: (num_samples, 1)

    # Create sequences
    X, y = [], []
    for i in range(sequence_length, len(close_scaled)):
        X.append(close_scaled[i-sequence_length:i, 0])  # Shape: (sequence_length,)
        y.append(close_scaled[i, 0])  # Target is the next 'Close' value

    # Convert to numpy arrays
    X = np.array(X)  # Shape: (num_samples, sequence_length)
    y = np.array(y)  # Shape: (num_samples,)

    # Reshape X to add the feature dimension
    X = X.reshape(X.shape[0], X.shape[1], 1)  # Shape: (num_samples, sequence_length, 1)

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test,scaler