# ssef_analysis_tool/main_window.py

# Import necessary PyQt5 classes for GUI components
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QMessageBox
)

# Import additional modules from other files within the project
from .sidebar import Sidebar
from .content_area import ContentArea
from .data_fetching import fetch_ticker_info
from .utils import format_number, currency_symbols
from .styles import MAIN_WINDOW_STYLE
import logging

# Configure logging to record error messages
logging.basicConfig(level=logging.ERROR)

class MainWindow(QMainWindow):
    """Main application window for the SSEF Analysis Tool."""

    def __init__(self):
        # Initialize the QMainWindow superclass
        super().__init__()
        
        # Set the title and size of the main application window
        self.setWindowTitle("SSEF - Analysis Tool")
        self.setGeometry(100, 100, 1700, 1100)

        # Initialize various attributes to be used throughout the application
        self.is_sidebar_expanded = True  # Sidebar starts as expanded
        self.active_button = None  # Keeps track of the currently active button in the sidebar
        self.currency = "$"  # Default currency symbol to use

        # Initialize the user interface and apply styles
        self.init_ui()
        self.apply_styles()

        # Variable to keep track of the currently selected stock ticker
        self.current_ticker = None

    def init_ui(self):
        """Initializes the UI components."""
        # Set the central widget for the main window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Use a horizontal box layout to organize the components of the main window
        self.main_layout = QHBoxLayout(self.central_widget)

        # Initialize Sidebar and Content Area, which are defined in separate files
        self.sidebar = Sidebar(self)  # Sidebar contains buttons for navigation
        self.content_area = ContentArea(self)  # ContentArea contains dynamic content widgets

        # Add Sidebar and Content Area to the main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

    def apply_styles(self):
        """Applies styles to the main window."""
        # Apply the specified stylesheet to the main window and the central widget
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.central_widget.setStyleSheet(MAIN_WINDOW_STYLE)

    def change_right_widget(self, widget_name):
        """Switches the main content area to display the selected widget."""
        # Highlight the active button in the sidebar based on the selected widget
        self.sidebar.highlight_active_button(widget_name)
        # Update the content area to display the corresponding widget
        self.content_area.display_widget(widget_name)

    def confirm_ticker(self, ticker):
        """Handles ticker confirmation, data fetching, and updates the content area."""
        # Ensure that the ticker input is not empty
        if not ticker:
            QMessageBox.critical(self, "Error", "Ticker box is empty")
            return

        try:
            # Fetch ticker information using the data_fetching module
            info = fetch_ticker_info(ticker)

            # Handle case where no information is found for the ticker
            if not info:
                QMessageBox.critical(self, "Error", f"No data found for ticker {ticker}")
                return

            # Set the current ticker attribute
            self.current_ticker = ticker

            # Update the window title to include the ticker symbol
            self.setWindowTitle(f"SSEF - Analysis Tool: {ticker}")

            # Update currency symbol based on ticker information
            currency_code = info.get('currency', 'USD')
            self.currency = currency_symbols.get(currency_code, currency_code)

            # Display the fetched ticker information in the content area
            self.display_ticker_info(info)

            # Update the chart widget to display data for the new ticker
            self.content_area.chart_widget.update_chart(ticker)

            # Switch the content area to display the "Information" view
            self.change_right_widget("Information")

        except Exception as e:
            # Log any exceptions that occur during data fetching
            logging.exception(f"Failed to retrieve data for ticker {ticker}")
            QMessageBox.critical(self, "Error", f"An error occurred while retrieving data for ticker {ticker}. Please try again later.")

    def display_ticker_info(self, info):
        """Displays the ticker information in the info text widget."""
        # Format the retrieved ticker information for display in the content area
        details = f"Name: {info.get('longName', 'N/A')}\n"
        details += f"Sector: {info.get('sector', 'N/A')}\n"
        details += f"Full Time Employees: {format_number(info.get('fullTimeEmployees', 'N/A'))}\n"
        details += f"Business Summary: {info.get('longBusinessSummary', 'N/A')}\n"
        details += f"Website: {info.get('website', 'N/A')}\n"
        details += f"Market Cap: {format_number(info.get('marketCap', 'N/A'), self.currency)}\n"
        details += f"PE Ratio: {info.get('forwardPE', 'N/A')}\n"
        
        # Format dividend yield if available, else display "N/A"
        dividend_yield = info.get('dividendYield')
        if dividend_yield:
            details += f"Dividend Yield: {dividend_yield * 100:.2f}%\n"
        else:
            details += "Dividend Yield: N/A\n"
        
        # Format book value if available
        details += f"Book Value: {format_number(info.get('bookValue', 'N/A'), self.currency)}\n"

        # Update the stock information in the content area with the formatted details
        self.content_area.update_stock_info(details)