# ssef_analysis_tool/utils.py

# Import necessary library for handling missing values in data
import pandas as pd

def format_number(num, currency="$"):
    """Formats a number with appropriate units and currency symbol.
    
    Args:
        num (float or int): The number to be formatted.
        currency (str, optional): The currency symbol to be used. Defaults to "$".
    
    Returns:
        str: The formatted number as a string with currency symbol and units (B for billion, M for million, K for thousand).
    """
    # Check if the number is NaN (Not a Number) and return "N/A" if true
    if pd.isna(num):
        return "N/A"

    # Determine if the number is negative, and work with its absolute value for formatting
    is_negative = num < 0
    num = abs(num)

    # Format the number based on its size (billions, millions, thousands, or less)
    if num >= 1e9:
        formatted_num = f'{currency} {num / 1e9:.2f} B'
    elif num >= 1e6:
        formatted_num = f'{currency} {num / 1e6:.2f} M'
    elif num >= 1e3:
        formatted_num = f'{currency} {num / 1e3:.2f} K'
    else:
        formatted_num = f'{currency} {num:.2f}'

    # Add parentheses for negative numbers to indicate a loss or deduction
    if is_negative:
        return f'({formatted_num})'
    else:
        return formatted_num

# Dictionary mapping currency codes to symbols for use in formatting
currency_symbols = {
    'USD': '$',  # US Dollar
    'EUR': '€',  # Euro
    'JPY': '¥',  # Japanese Yen
    'GBP': '£',  # British Pound
    'AUD': 'A$', # Australian Dollar
    'CAD': 'C$', # Canadian Dollar
    'HKD': 'HK$', # Hong Kong Dollar
    # Add more currencies as needed
}