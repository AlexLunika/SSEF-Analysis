# ssef_analysis_tool/simulations.py

# Import necessary libraries for simulation and threading
import numpy as np
import yfinance as yf
import threading
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QThread

class SimulationWorker(QObject):
    """Worker class to perform simulation in a separate thread."""
    # Define signals for when the simulation is finished or encounters an error
    finished = pyqtSignal(list)  # Emits a list of final prices
    error = pyqtSignal(str)  # Emits an error message

    def __init__(self, ticker):
        # Initialize the QObject superclass
        super().__init__()
        self.ticker = ticker  # Store the stock ticker symbol

    def run(self):
        """Performs the simulation and emits the result."""
        try:
            # Download historical prices for the past year with daily intervals
            hist_prices = yf.download(self.ticker, period='1y', interval='1d')
            if hist_prices.empty:
                # Emit an error if no historical data is found for the ticker
                self.error.emit(f"No historical data found for {self.ticker}")
                return

            # Calculate log returns based on closing prices
            log_returns = np.log(hist_prices['Close'] / hist_prices['Close'].shift(1)).dropna()
            # Get the latest closing price as the starting price for the simulation
            S0 = hist_prices['Close'].iloc[-1]
            # Calculate volatility (sigma) and mean return (mu) of the stock
            sigma = log_returns.std()
            mu = log_returns.mean() + sigma**2 / 2

            # Perform Geometric Brownian Motion (GBM) simulations
            final_prices = GBM(S0, mu, sigma)
            # Emit the simulation results
            self.finished.emit(final_prices)
        except Exception as e:
            # Emit an error message if an exception occurs during simulation
            self.error.emit(str(e))

def GBM(S0, mu, sigma, T=252, N=252, num_simulations=10000):
    """Performs Geometric Brownian Motion simulations.
    
    Args:
        S0 (float): The initial stock price.
        mu (float): The expected return of the stock.
        sigma (float): The volatility of the stock.
        T (int, optional): Total time period for the simulation (default is 252, representing one trading year).
        N (int, optional): Number of time steps within the time period (default is 252).
        num_simulations (int, optional): Number of simulation paths to generate (default is 10,000).
    
    Returns:
        list: A list of final stock prices for each simulation.
    """
    dt = T / N  # Time step size
    final_prices = []
    # Generate the simulations
    for _ in range(num_simulations):
        dW = np.sqrt(dt) * np.random.randn(N)  # Brownian increments
        W = np.cumsum(dW)  # Cumulative sum to simulate Brownian path
        t = np.linspace(0, T, N)  # Time steps
        # Calculate the stock price path using GBM formula
        stock_price = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)
        final_prices.append(stock_price[-1])  # Store the final price from the path
    return final_prices

class SimulationThread(threading.Thread):
    """Thread for running simulations without blocking the UI."""

    def __init__(self, S0, mu, sigma, callback):
        # Initialize the Thread superclass
        threading.Thread.__init__(self)
        self.S0 = S0  # Initial stock price
        self.mu = mu  # Expected return of the stock
        self.sigma = sigma  # Volatility of the stock
        self.callback = callback  # Callback function to call when the simulation is complete

    def run(self):
        """Runs the simulation and calls the callback with the result."""
        final_prices = GBM(self.S0, self.mu, self.sigma)  # Perform the simulation
        self.callback(final_prices)  # Call the callback function with the simulation results


def start_simulation(ticker, on_complete):
    """Starts the simulation in a separate thread.
    
    Args:
        ticker (str): The stock ticker symbol to perform the simulation for.
        on_complete (function): Callback function to call when the simulation is complete.
    """
    def run_simulation():
        """Nested function to run the simulation and ensure callback on the main thread."""
        # Download historical prices for the past year with daily intervals
        hist_prices = yf.download(ticker, period='1y', interval='1d')
        # Calculate log returns
        log_returns = np.log(hist_prices['Close'] / hist_prices['Close'].shift(1)).dropna()
        # Get the latest closing price as the starting price
        S0 = hist_prices['Close'].iloc[-1]
        # Calculate volatility (sigma) and mean return (mu)
        sigma = log_returns.std()
        mu = log_returns.mean() + sigma**2 / 2

        # Perform Geometric Brownian Motion (GBM) simulations
        final_prices = GBM(S0, mu, sigma)
        # Ensure callback is called on the main thread using QTimer
        QTimer.singleShot(0, lambda: on_complete(final_prices))

    # Start the simulation in a new thread
    threading.Thread(target=run_simulation).start()