# ssef_analysis_tool/styles.py

# Import necessary PyQt5 class for font customization
from PyQt5.QtGui import QFont

# Main window style settings
MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #00111a;
}
"""
# This style sets the background color of the main window to a dark shade (#00111a).

# Sidebar style settings
SIDEBAR_STYLE = """
QWidget {
    background-color: #00111a;
}
"""
# This style sets the background color of the sidebar to match the main window, ensuring visual consistency.

# Button style settings for navigation and toggle buttons
BUTTON_STYLE = """
QPushButton {
    color: white;
    background-color: #001933;
    border: none;
    padding: 5px;
    border-radius: 2px;
    margin: 2px;
}
QPushButton:hover {
    background-color: #002d4d;
}
QPushButton:pressed {
    background-color: #001f2d;
}
"""
# The BUTTON_STYLE applies to regular navigation buttons:
# - Background color is a dark blue (#001933) and changes to a lighter blue on hover (#002d4d).
# - On pressing the button, it becomes slightly darker (#001f2d).
# - White text color, rounded corners, and padding give a polished look.

# Active button style settings for the currently selected navigation button
ACTIVE_BUTTON_STYLE = """
QPushButton {
    color: white;
    background-color: #002d4d;
    border: none;
    padding: 5px;
    border-radius: 2px;
    margin: 2px;
}
"""
# ACTIVE_BUTTON_STYLE is applied to the currently active button:
# - The background color is set to #002d4d to differentiate from inactive buttons.

# Text edit widget style settings
TEXT_EDIT_STYLE = """
QTextEdit {
    background-color: #00111a;
    color: white;
    border: 1px solid #004466;
    padding: 5px;
    border-radius: 2px;
    font-family: 'Consolas';
    font-size: 10pt;
}
"""
# TEXT_EDIT_STYLE customizes the appearance of QTextEdit widgets:
# - Background color is set to a dark theme to match the application style.
# - White text color ensures readability.
# - Consolas font is used with a 10pt size to provide a clear, code-like appearance.

# Table widget style settings
TABLE_STYLE = """
QTableWidget {
    background-color: #00111a;
    color: white;
    gridline-color: #003344;
}
QHeaderView::section {
    background-color: #001933;
    color: white;
    padding: 4px;
    border: 1px solid #004466;
    font-size: 10pt;
}
QTableCornerButton::section {
    background-color: #001933;  /* Match the header background */
    border: 1px solid #004466;  /* Match the header border */
}
QTableWidget::item {
    padding: 5px;
    border-color: #004466;
}
QTableWidget::item:selected {
    background-color: #002d4d;
}
"""
# TABLE_STYLE is used to customize QTableWidget components:
# - The dark theme is maintained for the table background and grid lines.
# - The header sections are styled separately to stand out with a lighter shade and a 1px solid border.
# - Selected items are highlighted with a different background color (#002d4d).

# Content area style settings
CONTENT_AREA_STYLE = """
QWidget {
    background-color: #00111a;
}
"""
# CONTENT_AREA_STYLE is used for the content area widgets to ensure they have the same dark background color as the rest of the application.

# Simulation chart styles
CHART_BACKGROUND_COLOR = "#00111a"  # Background color for charts
CHART_TITLE_COLOR = "#ffffff"  # White color for chart titles
CHART_AXIS_LABEL_COLOR = "#ffffff"  # White color for axis labels
CHART_AXIS_LINE_COLOR = "#004466"  # Blue color for axis lines
CHART_GRID_LINE_COLOR = "#003344"  # Color for grid lines to match theme
CHART_SERIES_COLOR = "#00ccff"  # Color for the main series in charts
CHART_SERIES_PEN_WIDTH = 2  # Pen width for series lines
PDF_SERIES_COLOR = "#00ccff"  # Color for Probability Density Function (PDF) series in charts
CDF_SERIES_COLOR = "#ff66cc"  # Color for Cumulative Distribution Function (CDF) series in charts

# Font settings for charts
CHART_TITLE_FONT = QFont("Arial", 12, QFont.Bold)  # Bold Arial font, size 12 for chart titles
CHART_LABEL_FONT = QFont("Arial", 10)  # Arial font, size 10 for chart labels