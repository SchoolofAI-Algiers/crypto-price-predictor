import tensorflow as tf
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler


class Model():
    def __init__(self,units,n_in):
        self.units=units
        self.n_in=n_in
        self.model=None

    
    # def define_model(self):
    #     model=Sequential()
    #     model.add(LSTM(self.units, activation='tanh', input_shape=(self.n_in,1)))
    #     model.add(Dense(1))
    #     model.compile(optimizer='adam', loss='mse')
    #     self.model=model

 

    def define_model(self):
        """
        Define an LSTM autoencoder model using the Sequential API.

        Args:
            self.n_in (int): Number of input time steps.
        """
        # Define the model
        model = Sequential()

        # Encoder
        model.add(LSTM(self.units, activation='relu', input_shape=(self.n_in, 1)))
        model.add(LSTM(self.units//2, activation='relu', input_shape=(self.n_in, 1)))

        # RepeatVector to match the input sequence length
        model.add(RepeatVector(self.n_in))

        # Decoder
        model.add(LSTM(self.units, activation='relu', return_sequences=True))
        model.add(TimeDistributed(Dense(1)))

        # Compile the model
        model.compile(optimizer='adam', loss='mse')

        # Assign the model to self.model
        self.model = model


    def train(self,X_train,y_train, batch_size=32,epochs=40):
        hist=self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
        self.model.save("models/LSTMAutoencoder_RELU_128.h5")
        return hist
    
    def evaluation(self, history, X_test, y_test,scaler):
        """
        Evaluate the model and plot the training loss and actual vs predicted values.

        Args:
            history: Training history returned by `model.fit()`.
            X_test: Test input data.
            y_test: Test target data.
            scaler: Fitted MinMaxScaler instance used during preprocessing.
        """
        # Evaluate the model
        loss = self.model.evaluate(X_test, y_test, verbose=1)
        print(f"Test Loss: {loss}")

        # Plot training loss
        plt.figure(figsize=(8, 5))
        plt.plot(history.history['loss'], label='Training Loss')
        plt.title('Training Loss Over Epochs')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.savefig('plots/loss_RELU_128.png')

        y_pred = self.model.predict(X_test)
        y_pred=y_pred[:, -1, 0] 
        y_pred=scaler.inverse_transform(y_pred.reshape(-1,1))
        y_test=scaler.inverse_transform(y_test.reshape(-1,1))

        plt.figure(figsize=(20, 10))
        plt.plot(y_test, label='Actual Values', color='blue')
        plt.plot(y_pred, label='Predicted Values', color='red', linestyle='--')
        plt.title('Actual vs Predicted Values')
        plt.xlabel('Time Steps')
        plt.ylabel('Close Price')
        plt.legend()
        plt.grid(True)
        plt.savefig('plots/actual_vs_predicted_RELU_128.png')
