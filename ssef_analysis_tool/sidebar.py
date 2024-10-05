# ssef_analysis_tool/sidebar.py

# Import necessary PyQt5 classes for GUI components
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QSizePolicy, QLayout
)
from PyQt5.QtCore import Qt
from functools import partial

# Import styles used in the sidebar from other files within the project
from .styles import SIDEBAR_STYLE, BUTTON_STYLE, ACTIVE_BUTTON_STYLE

class Sidebar(QWidget):
    """Sidebar widget containing navigation buttons and search functionality."""

    def __init__(self, parent=None):
        # Initialize the QWidget superclass
        super().__init__(parent)
        self.parent = parent  # Reference to MainWindow
        self.is_expanded = True  # Track whether the sidebar is expanded or collapsed
        self.active_button = None  # Track the currently active button

        # Initialize the user interface and apply styles
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Initializes the sidebar UI components."""
        # Use a vertical layout for organizing components
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)  # Align layout to the top of the sidebar

        # Toggle Sidebar Button: Used to expand or collapse the sidebar
        self.toggle_button = QPushButton("<<")
        self.toggle_button.clicked.connect(self.toggle_sidebar)  # Connect button click to toggle_sidebar method
        self.layout.addWidget(self.toggle_button)

        # Ticker Entry: Input field for searching stock tickers
        self.ticker_entry = QLineEdit()
        self.ticker_entry.setPlaceholderText("Search Ticker")  # Placeholder text
        self.ticker_entry.returnPressed.connect(self.confirm_ticker)  # Connect enter key press to confirm_ticker method
        self.layout.addWidget(self.ticker_entry)

        # Navigation Buttons: Buttons for navigating different sections of the application
        self.buttons = []
        labels = [
            'Information', 'Graphs', 'Income Statement', 'Balance Sheet',
            'Cash Flow', 'Risk Statistics', 'Simulate Prices'
        ]
        for label in labels:
            button = QPushButton(label)  # Create a button for each label
            button.clicked.connect(partial(self.parent.change_right_widget, label))  # Connect button click to parent method
            self.layout.addWidget(button)  # Add the button to the layout
            self.buttons.append(button)  # Store button in list for later use

        # Set size policies to control the size and resizing behavior of the components
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.setSizeConstraint(QLayout.SetMinimumSize)
        for button in self.buttons:
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.toggle_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.ticker_entry.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def apply_styles(self):
        """Applies styles to the sidebar and its components."""
        # Apply the specified stylesheet to the sidebar
        self.setStyleSheet(SIDEBAR_STYLE)
        # Apply button style to the toggle button
        self.toggle_button.setStyleSheet(BUTTON_STYLE)
        # Apply button style to each navigation button
        for button in self.buttons:
            button.setStyleSheet(BUTTON_STYLE)
        # Apply style to the ticker entry field
        self.ticker_entry.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #004466;
                padding: 5px;
                border-radius: 2px;
            }
        """)

    def toggle_sidebar(self):
        """Toggles the sidebar's visibility."""
        if self.is_expanded:
            # Collapse the sidebar
            self.toggle_button.setText(">>")
            self.setFixedWidth(50)  # Set sidebar to a smaller width
            # Hide buttons and ticker entry when collapsed
            self.ticker_entry.hide()
            for button in self.buttons:
                button.hide()
        else:
            # Expand the sidebar
            self.toggle_button.setText("<<")
            self.setFixedWidth(200)  # Set sidebar to full width
            # Show buttons and ticker entry when expanded
            self.ticker_entry.show()
            for button in self.buttons:
                button.show()
        # Update the expanded state
        self.is_expanded = not self.is_expanded

    def confirm_ticker(self):
        """Handles ticker confirmation and delegates to MainWindow."""
        # Get the ticker symbol entered by the user
        ticker = self.ticker_entry.text().strip().upper()
        if not ticker:
            # Show error message if the ticker input is empty
            QMessageBox.critical(self, "Error", "Ticker box is empty")
            return
        # Call the method in MainWindow to handle ticker confirmation
        self.parent.confirm_ticker(ticker)

    def highlight_active_button(self, widget_name):
        """Highlights the active navigation button."""
        for button in self.buttons:
            if button.text() == widget_name:
                # Apply the active button style if the button matches the current view
                button.setStyleSheet(ACTIVE_BUTTON_STYLE)
            else:
                # Apply the default button style for inactive buttons
                button.setStyleSheet(BUTTON_STYLE)