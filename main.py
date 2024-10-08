# main.py

# Importing necessary modules
import sys  # The sys module provides access to system-specific parameters and functions.
from PyQt5.QtWidgets import QApplication  # Importing QApplication from PyQt5, a necessary class for GUI applications.
from ssef_analysis_tool.main_window import MainWindow  # Importing MainWindow class from the custom module, which contains the main interface of the application.

# Entry point of the application
if __name__ == "__main__":
    # Creating an instance of QApplication, which manages the GUI application's control flow and settings.
    app = QApplication(sys.argv)  # QApplication takes command-line arguments via sys.argv.
    
    try:
        # Creating an instance of the main application window.
        window = MainWindow()  # MainWindow is the main GUI component of the application.
        
        # Displaying the main application window to the user.
        window.show()  # show() makes the main window visible.
        
        # Execute the application's main event loop, allowing it to run and wait for user interactions.
        sys.exit(app.exec_())  # app.exec_() starts the Qt event loop, and sys.exit ensures a proper exit code when the app is closed.
    
    except Exception as e:
        # Handling any unexpected errors during the application's runtime.
        print(f"An unexpected error occurred: {e}")  # Printing the error message to the console for debugging purposes.
        sys.exit(1)  # Exiting the application with a non-zero code to indicate failure.