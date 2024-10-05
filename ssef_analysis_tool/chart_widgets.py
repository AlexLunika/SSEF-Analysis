# ssef_analysis_tool/chart_widgets.py

# Import necessary PyQt5 classes for GUI components
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QAreaSeries, QValueAxis
from PyQt5.QtGui import QPen, QColor, QBrush, QLinearGradient, QPainter
from lightweight_charts.widgets import QtChart
import yfinance as yf
import datetime as dt
import numpy as np

# Import additional styles used for charts from other files within the project
from .styles import (
    CHART_BACKGROUND_COLOR, CHART_TITLE_COLOR, CHART_AXIS_LABEL_COLOR,
    CHART_AXIS_LINE_COLOR, CHART_GRID_LINE_COLOR, CHART_SERIES_COLOR,
    CHART_SERIES_PEN_WIDTH, CHART_TITLE_FONT, CHART_LABEL_FONT, PDF_SERIES_COLOR, CDF_SERIES_COLOR
)

class LightweightChartWidget(QWidget):
    """Widget for displaying financial charts using lightweight-charts."""

    def __init__(self, parent=None):
        # Initialize the QWidget superclass
        super().__init__(parent)
        self.init_ui()  # Initialize the user interface components
        self.data_cache = {}  # Cache for storing fetched data to avoid redundant API calls

    def init_ui(self):
        """Initializes the chart widget UI."""
        # Set widget dimensions
        self.resize(800, 500)
        layout = QVBoxLayout(self)  # Use vertical layout for the chart widget

        # Initialize the main chart view
        self.chart = QtChart()  # Lightweight chart component
        layout.addWidget(self.chart.get_webview())  # Add the chart view to the layout

        # Create buttons for different timeframes to view chart data
        bottom_bar_layout = QHBoxLayout()
        timeframes = ['1m', '5m', '30m', '1wk']
        self.buttons = {}
        for tf in timeframes:
            button = QPushButton(tf)  # Create a button for each timeframe
            button.clicked.connect(lambda _, tf=tf: self.on_timeframe_selection(tf))  # Connect button click to function
            bottom_bar_layout.addWidget(button)  # Add button to bottom bar layout
            self.buttons[tf] = button  # Store button in a dictionary for easy access

        layout.addLayout(bottom_bar_layout)  # Add the bottom bar with buttons to the main layout

        # Set default values for the current timeframe and ticker
        self.current_timeframe = '5m'
        self.current_ticker = ''
        self.update_button_styles()  # Update styles for the buttons

    def update_chart(self, ticker):
        """Updates the chart to display data for the given ticker symbol."""
        self.current_ticker = ticker.upper()  # Update the current ticker
        success = self.get_bar_data(self.current_ticker, self.current_timeframe)  # Fetch and display data
        if not success:
            print(f"Failed to update chart for ticker: {ticker}")  # Log error if data fetching fails
            # Optionally display an error message or clear the chart

    def get_bar_data(self, ticker, timeframe):
        """Fetches and updates the chart with bar data for a specific ticker and timeframe."""
        print(f"Fetching data for ticker: {ticker}, timeframe: {timeframe}")
        cache_key = f"{ticker}_{timeframe}"  # Create a unique key for caching data
        
        # Check if data is already cached to avoid redundant API calls
        if cache_key in self.data_cache:
            data = self.data_cache[cache_key]
            print("Using cached data")
        else:
            # Determine the start date based on the selected timeframe
            if timeframe in ('1m', '5m', '30m'):
                days = 7 if timeframe == '1m' else 60
                start = dt.datetime.now() - dt.timedelta(days=days)
            else:
                start = None

            # Fetch data using yfinance
            data = yf.download(ticker, start=start, interval=timeframe)
            if data.empty:
                print(f"No data found for {ticker}")  # Log if no data is found
                return False

            self.data_cache[cache_key] = data  # Cache the fetched data

        # Update the chart with the new data
        self.chart.set(data)
        print(f"Chart updated for ticker: {ticker}")
        return True

    def on_timeframe_selection(self, timeframe):
        """Handles timeframe selection when a button is clicked."""
        self.current_timeframe = timeframe  # Update the current timeframe
        if self.current_ticker:
            self.update_chart(self.current_ticker)  # Update the chart for the selected timeframe
        self.update_button_styles()  # Update button styles to highlight active timeframe

    def update_button_styles(self):
        """Updates the styles of the timeframe buttons."""
        for tf, button in self.buttons.items():
            if tf == self.current_timeframe:
                # Apply active button style for the selected timeframe
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #002d4d;
                        color: white;
                        border: none;
                        padding: 5px;
                        border-radius: 2px;
                        margin: 2px;
                    }
                """)
            else:
                # Apply default button style for other timeframes
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #001933;
                        color: white;
                        border: none;
                        padding: 5px;
                        border-radius: 2px;
                        margin: 2px;
                    }
                """)

class QtChartsWidget(QWidget):
    """Widget for displaying charts using PyQt5's QtChart."""

    def __init__(self, parent=None):
        # Initialize the QWidget superclass
        super().__init__(parent)
        self.init_ui()  # Initialize the user interface components

    def init_ui(self):
        """Initializes the QtCharts widget UI."""
        self.layout = QVBoxLayout(self)  # Use vertical layout for the widget
        self.pdf_chart_view = QChartView()  # Create chart view for PDF (Probability Density Function)
        self.cdf_chart_view = QChartView()  # Create chart view for CDF (Cumulative Distribution Function)

        # Add the PDF and CDF chart views to the layout
        self.layout.addWidget(self.pdf_chart_view)
        self.layout.addWidget(self.cdf_chart_view)

    def plot_simulation_results(self, final_prices, ticker, currency):
        """Plots the simulation results using PDF and CDF charts."""
        # Calculate histogram data for PDF and CDF
        hist, bins = np.histogram(final_prices, bins=50)
        pdf = hist / sum(hist)  # Calculate probability density function (PDF)
        cdf = np.cumsum(pdf)  # Calculate cumulative distribution function (CDF)
        pdf_smooth = np.convolve(pdf, np.ones(5)/5, mode='same')  # Smooth the PDF for better visualization

        stock_name = ticker.upper()  # Get the stock name in uppercase

        # Plot PDF chart
        self.plot_pdf(bins[:-1], pdf_smooth, stock_name, currency)

        # Plot CDF chart
        self.plot_cdf(bins[:-1], cdf, stock_name, currency)

    def plot_pdf(self, bins, pdf_smooth, stock_name, currency):
        """Plots the Probability Density Function (PDF)."""
        # Clear previous chart
        pdf_chart = QChart()
        pdf_chart.legend().hide()  # Hide legend for PDF
        pdf_chart.setTitle(f"{stock_name} - PDF of Simulated Prices")
        pdf_chart.setTitleFont(CHART_TITLE_FONT)
        pdf_chart.setTitleBrush(QColor(CHART_TITLE_COLOR))
        pdf_chart.setBackgroundBrush(QColor(CHART_BACKGROUND_COLOR))

        # Create and configure the PDF series
        pdf_series = QLineSeries()
        pen = QPen(QColor(PDF_SERIES_COLOR))
        pen.setWidth(CHART_SERIES_PEN_WIDTH)
        pdf_series.setPen(pen)

        # Add data points to the PDF series
        for x, y in zip(bins, pdf_smooth):
            pdf_series.append(x, y)

        # Add the series to the chart
        pdf_chart.addSeries(pdf_series)

        # Create default axes and customize them
        pdf_chart.createDefaultAxes()
        axis_x = pdf_chart.axes(Qt.Horizontal)[0]
        axis_y = pdf_chart.axes(Qt.Vertical)[0]
        self.customize_axis(axis_x)
        self.customize_axis(axis_y)

        # Set axes labels and fonts
        axis_x.setTitleText(f"Price ({currency})")
        axis_y.setTitleText("Probability")
        axis_x.setTitleFont(CHART_LABEL_FONT)
        axis_y.setTitleFont(CHART_LABEL_FONT)
        axis_x.setLabelsFont(CHART_LABEL_FONT)
        axis_y.setLabelsFont(CHART_LABEL_FONT)

        # Set the updated chart to the chart view
        self.pdf_chart_view.setChart(pdf_chart)
        self.pdf_chart_view.setRenderHint(QPainter.Antialiasing)

    def plot_cdf(self, bins, cdf, stock_name, currency):
        """Plots the Cumulative Distribution Function (CDF)."""
        # Clear previous chart
        cdf_chart = QChart()
        cdf_chart.legend().hide()  # Hide legend for CDF
        cdf_chart.setTitle(f"{stock_name} - CDF of Simulated Prices")
        cdf_chart.setTitleFont(CHART_TITLE_FONT)
        cdf_chart.setTitleBrush(QColor(CHART_TITLE_COLOR))
        cdf_chart.setBackgroundBrush(QColor(CHART_BACKGROUND_COLOR))

        # Create and configure the CDF series
        cdf_series = QLineSeries()
        pen = QPen(QColor(CDF_SERIES_COLOR))
        pen.setWidth(CHART_SERIES_PEN_WIDTH)
        cdf_series.setPen(pen)

        # Add data points to the CDF series
        for x, y in zip(bins, cdf):
            cdf_series.append(x, y)

        # Add the series to the chart
        cdf_chart.addSeries(cdf_series)

        # Create default axes and customize them
        cdf_chart.createDefaultAxes()
        axis_x = cdf_chart.axes(Qt.Horizontal)[0]
        axis_y = cdf_chart.axes(Qt.Vertical)[0]
        self.customize_axis(axis_x)
        self.customize_axis(axis_y)

        # Set axes labels and fonts
        axis_x.setTitleText(f"Price ({currency})")
        axis_y.setTitleText("Cumulative Probability")
        axis_x.setTitleFont(CHART_LABEL_FONT)
        axis_y.setTitleFont(CHART_LABEL_FONT)
        axis_x.setLabelsFont(CHART_LABEL_FONT)
        axis_y.setLabelsFont(CHART_LABEL_FONT)

        # Set the updated chart to the chart view
        self.cdf_chart_view.setChart(cdf_chart)
        self.cdf_chart_view.setRenderHint(QPainter.Antialiasing)

    def customize_axis(self, axis):
        """Customizes the appearance of an axis."""
        # Set axis line color
        axis.setLinePen(QPen(QColor(CHART_AXIS_LINE_COLOR)))

        # Set axis label color
        axis.setLabelsBrush(QColor(CHART_AXIS_LABEL_COLOR))

        # Set grid line color and style
        grid_pen = QPen(QColor(CHART_GRID_LINE_COLOR))
        grid_pen.setStyle(Qt.SolidLine)
        axis.setGridLinePen(grid_pen)

        # Set minor grid lines
        minor_grid_pen = QPen(QColor(CHART_GRID_LINE_COLOR))
        minor_grid_pen.setStyle(Qt.DotLine)
        axis.setMinorGridLinePen(minor_grid_pen)

        # Set tick labels font
        axis.setLabelsFont(CHART_LABEL_FONT)

        # Enable grid lines
        axis.setGridLineVisible(True)
        axis.setMinorGridLineVisible(True)

class CustomChartView(QChartView):
    """Custom chart view with crosshair and tooltips."""

    def __init__(self, parent=None):
        # Initialize the QChartView superclass
        super().__init__(parent)
        # Custom initialization logic can be added here
        pass

    # Additional methods for event handling and drawing (crosshairs, tooltips, etc.) can be implemented here