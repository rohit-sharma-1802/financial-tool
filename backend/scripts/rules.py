# rules.py

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

# This function is already provided.
def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    try:
        financials = data['financials'][financial_index]
        return financials['pnl']['lineItems']['netRevenue']['value']
    except KeyError:
        return 0.0

def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total borrowings to total revenue.
    """
    try:
        financials = data['financials'][financial_index]
        long_term_borrowings = financials['bs']['lineItems']['longTermBorrowings']['value']
        short_term_borrowings = financials['bs']['lineItems']['shortTermBorrowings']['value']
        total_borrowings = long_term_borrowings + short_term_borrowings
        revenue = total_revenue(data, financial_index)
        return total_borrowings / revenue if revenue != 0 else 0.0
    except KeyError:
        return 0.0

def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.
    
    ISCR is calculated as (EBIT + Depreciation + 1) / (Interest Expenses + 1).
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    try:
        financials = data['financials'][financial_index]
        ebit = financials['pnl']['lineItems']['ebit']['value']
        depreciation = financials['pnl']['lineItems']['depreciation']['value']
        interest_expenses = financials['pnl']['lineItems']['interestExpenses']['value']
        iscr_value = (ebit + depreciation + 1) / (interest_expenses + 1)
        return iscr_value
    except KeyError:
        return 0.0

def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ISCR value.
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million (5 Crore).
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50_000_000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.
    
    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER

def apply_rules(data):
    """
    Apply all the financial rules on the provided data.
    
    Parameters:
    - data (dict): A dictionary containing financial data.

    Returns:
    - dict: A dictionary with the results of applied rules.
    """
    financial_index = latest_financial_index(data)
    
    results = {
        "total_revenue": total_revenue(data, financial_index),
        "total_borrowing_to_revenue_ratio": total_borrowing(data, financial_index),
        "iscr_value": iscr(data, financial_index),
        "iscr_flag": iscr_flag(data, financial_index),
        "total_revenue_5cr_flag": total_revenue_5cr_flag(data, financial_index),
        "borrowing_to_revenue_flag": borrowing_to_revenue_flag(data, financial_index)
    }
    
    return results
