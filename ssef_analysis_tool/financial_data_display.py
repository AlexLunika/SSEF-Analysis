# ssef_analysis_tool/financial_data_display.py

# Import necessary libraries
import pandas as pd
from .utils import format_number
from PyQt5.QtWidgets import QTableWidgetItem

def display_financial_data(table_widget, dataframe, currency="$"):
    """Displays financial data in a QTableWidget.
    
    Args:
        table_widget (QTableWidget): The table widget in which to display the financial data.
        dataframe (pd.DataFrame): The DataFrame containing the financial data to display.
        currency (str, optional): The currency symbol to use for formatting the values. Defaults to "$".
    """
    # Ensure the table is cleared before displaying new data
    table_widget.clear()

    # Return immediately if the DataFrame is empty
    if dataframe.empty:
        return

    # Set up the table dimensions and headers based on the DataFrame
    table_widget.setColumnCount(len(dataframe.columns))  # Set the number of columns
    table_widget.setRowCount(len(dataframe.index))  # Set the number of rows
    table_widget.setHorizontalHeaderLabels(dataframe.columns.astype(str))  # Set column headers
    table_widget.setVerticalHeaderLabels(dataframe.index.astype(str))  # Set row headers

    # Populate the table with data from the DataFrame
    for row in range(dataframe.shape[0]):
        for col in range(dataframe.shape[1]):
            # Format the cell value using the format_number utility
            value = format_number(dataframe.iat[row, col], currency)
            # Create a table widget item with the formatted value
            item = QTableWidgetItem(value)
            # Set the item at the specified row and column
            table_widget.setItem(row, col, item)

    # Resize columns to fit the contents
    table_widget.resizeColumnsToContents()