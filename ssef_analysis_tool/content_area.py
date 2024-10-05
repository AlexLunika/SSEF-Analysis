# ssef_analysis_tool/content_area.py

# Import necessary PyQt5 classes for GUI components
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget, QTextEdit, QTableWidget, QMessageBox
)
from PyQt5.QtCore import QThread

# Import additional modules from other files within the project
from .chart_widgets import LightweightChartWidget, QtChartsWidget
from .simulations import SimulationWorker
from .styles import CONTENT_AREA_STYLE, TEXT_EDIT_STYLE, TABLE_STYLE

class ContentArea(QWidget):
    """Main content area that displays different widgets."""

    def __init__(self, parent=None):
        # Initialize the QWidget superclass
        super().__init__(parent)
        self.parent = parent  # Reference to MainWindow

        # Initialize the user interface and apply styles
        self.init_ui()
        self.apply_styles()

        # Attribute to store current stock information text
        self.stock_info_text = ""

        # Attributes for managing threading during simulations
        self.simulation_thread = None
        self.simulation_worker = None

    def init_ui(self):
        """Initializes the content area UI components."""
        # Use a vertical box layout for the content area
        self.layout = QVBoxLayout(self)

        # Use a stacked widget to allow switching between different views
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Initialize different views for content display
        self.info_text = QTextEdit()  # Widget for displaying text information
        self.info_text.setReadOnly(True)  # Make the text edit read-only
        self.stack.addWidget(self.info_text)  # Add to the stacked widget

        self.chart_widget = LightweightChartWidget()  # Widget for displaying charts
        self.stack.addWidget(self.chart_widget)  # Add chart widget to the stack

        self.financial_table = QTableWidget()  # Widget for displaying financial data tables
        self.stack.addWidget(self.financial_table)  # Add table widget to the stack

        self.simulation_chart = None  # Placeholder for simulation chart (initialized later)

    def apply_styles(self):
        """Applies styles to the content area and its components."""
        # Apply the specified stylesheet to the content area and its widgets
        self.setStyleSheet(CONTENT_AREA_STYLE)
        self.info_text.setStyleSheet(TEXT_EDIT_STYLE)
        self.financial_table.setStyleSheet(TABLE_STYLE)

    def update_stock_info(self, text):
        """Updates the stock information and stores it."""
        # Store the updated stock information text
        self.stock_info_text = text
        # Update the text displayed in the info_text widget
        self.info_text.setText(text)

    def update_info_text(self, text):
        """Updates the information text view without altering stored stock info."""
        # Update the info_text widget without changing the stored stock information
        self.info_text.setText(text)

    def display_widget(self, widget_name):
        """Displays the specified widget in the content area."""
        # Display the corresponding widget based on the widget name
        if widget_name == "Information":
            self.info_text.setText(self.stock_info_text)
            self.stack.setCurrentWidget(self.info_text)
        elif widget_name == "Graphs":
            self.stack.setCurrentWidget(self.chart_widget)
        elif widget_name == "Income Statement":
            self.display_financial_statement('income')
            self.stack.setCurrentWidget(self.financial_table)
        elif widget_name == "Balance Sheet":
            self.display_financial_statement('balance')
            self.stack.setCurrentWidget(self.financial_table)
        elif widget_name == "Cash Flow":
            self.display_financial_statement('cash_flow')
            self.stack.setCurrentWidget(self.financial_table)
        elif widget_name == "Risk Statistics":
            self.display_risk_statistics()
        elif widget_name == "Simulate Prices":
            self.run_simulation()
        else:
            # Handle other widgets or show a default view (not implemented)
            pass

    def display_financial_statement(self, statement_type):
        """Displays the financial statement in the table widget."""
        # Retrieve the current ticker from the parent MainWindow
        ticker = self.parent.current_ticker
        if not ticker:
            # Display warning if no ticker is selected
            QMessageBox.warning(self, "Warning", "Please enter a valid ticker symbol.")
            return

        # Fetch financial data for the specified statement type
        from .data_fetching import fetch_financial_statement
        dataframe = fetch_financial_statement(ticker, statement_type)

        # Display warning if the dataframe is empty (no data found)
        if dataframe.empty:
            QMessageBox.warning(
                self,
                "Warning",
                f"No data available for {statement_type.replace('_', ' ').title()}.",
            )
            return

        # Update the table widget with the fetched financial data
        from .financial_data_display import display_financial_data
        display_financial_data(self.financial_table, dataframe, currency=self.parent.currency)

        # Re-apply the stylesheet to ensure correct styles after updating the table
        self.financial_table.setStyleSheet(TABLE_STYLE)

        # Switch to the table view to display financial data
        self.stack.setCurrentWidget(self.financial_table)

    def display_risk_statistics(self):
        """Displays risk statistics in the info text widget."""
        # Retrieve the current ticker from the parent MainWindow
        ticker = self.parent.current_ticker
        if not ticker:
            # Display warning if no ticker is selected
            QMessageBox.warning(self, "Warning", "Please enter a valid ticker symbol.")
            return

        # Fetch risk data such as beta value
        from .data_fetching import fetch_ticker_info
        info = fetch_ticker_info(ticker)

        # Format and display the risk statistics
        beta = info.get('beta', 'N/A')
        risk_message = f"Beta for {ticker}: {beta}"
        self.update_info_text(risk_message)
        self.stack.setCurrentWidget(self.info_text)

    def run_simulation(self):
        """Runs the GBM (Geometric Brownian Motion) simulation and displays the results."""
        # Retrieve the current ticker from the parent MainWindow
        ticker = self.parent.current_ticker
        if not ticker:
            # Display warning if no ticker is selected
            QMessageBox.warning(self, "Warning", "Please enter a valid ticker symbol.")
            return

        # Display a loading message while the simulation is running
        self.update_info_text("Running simulation...")
        self.stack.setCurrentWidget(self.info_text)

        # Start the simulation in a new thread to avoid blocking the UI
        self.simulation_thread = QThread()
        self.simulation_worker = SimulationWorker(ticker)
        self.simulation_worker.moveToThread(self.simulation_thread)

        # Connect signals to manage thread start, completion, and error handling
        self.simulation_thread.started.connect(self.simulation_worker.run)
        self.simulation_worker.finished.connect(self.on_simulation_complete)
        self.simulation_worker.error.connect(self.on_simulation_error)
        self.simulation_worker.finished.connect(self.simulation_thread.quit)
        self.simulation_worker.finished.connect(self.simulation_worker.deleteLater)
        self.simulation_thread.finished.connect(self.simulation_thread.deleteLater)

        # Start the simulation thread
        self.simulation_thread.start()

    def on_simulation_complete(self, final_prices):
        """Callback function when simulation is complete."""
        # Initialize the simulation chart if it hasn't been created yet
        if self.simulation_chart is None:
            self.simulation_chart = QtChartsWidget()
            self.stack.addWidget(self.simulation_chart)

        # Plot the simulation results on the chart widget
        self.simulation_chart.plot_simulation_results(
            final_prices, self.parent.current_ticker, self.parent.currency
        )
        # Switch to the simulation chart view
        self.stack.setCurrentWidget(self.simulation_chart)

    def on_simulation_error(self, error_message):
        """Handles errors during simulation."""
        # Display error message in a dialog box
        QMessageBox.critical(self, "Simulation Error", error_message)
        # Update the information text to indicate the simulation failed
        self.update_info_text("Simulation failed.")