# ssef_analysis_tool/data_fetching.py

# Import necessary libraries for data fetching
import yfinance as yf
import pandas as pd

def fetch_ticker_info(ticker):
    """Fetches ticker information from Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol to fetch information for.
        
    Returns:
        dict: A dictionary containing the stock's information, such as its name, market cap, sector, etc.
    """
    # Create an instance of the Ticker class from yfinance for the given ticker symbol
    stock = yf.Ticker(ticker)
    
    # Get the stock information in the form of a dictionary
    info = stock.info
    
    # Return the stock information
    return info

def fetch_financial_statement(ticker, statement_type):
    """Fetches financial statements (income, balance sheet, cash flow) and reorders columns.
    
    Args:
        ticker (str): The stock ticker symbol to fetch financial data for.
        statement_type (str): The type of financial statement to fetch ('income', 'balance', 'cash_flow').
        
    Returns:
        pd.DataFrame: A DataFrame containing the financial statement data, with columns arranged from oldest to newest.
    """
    # Create an instance of the Ticker class from yfinance for the given ticker symbol
    stock = yf.Ticker(ticker)
    
    # Determine which type of financial statement to fetch
    if statement_type == 'income':
        dataframe = stock.financials  # Fetch income statement
    elif statement_type == 'balance':
        dataframe = stock.balance_sheet  # Fetch balance sheet
    elif statement_type == 'cash_flow':
        dataframe = stock.cashflow  # Fetch cash flow statement
    else:
        return pd.DataFrame()  # Return an empty DataFrame if an unsupported statement type is provided
    
    # Return empty DataFrame if no data is available
    if dataframe.empty:
        return dataframe

    # Reverse the columns to arrange them from oldest to newest
    dataframe = dataframe.iloc[:, ::-1]
    
    # Return the processed DataFrame
    return dataframe