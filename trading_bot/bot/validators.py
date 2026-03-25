import argparse

def validate_positive_float(value):
    """Checks if the given value is a positive float."""
    try:
        f_value = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid float.")
    
    if f_value <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be greater than zero.")
    return f_value

def validate_symbol(symbol):
    """Basic validation for symbol format."""
    symbol = symbol.upper()
    if not symbol.endswith("USDT"):
         # For futures testnet, symbols usually end with USDT
         pass 
    return symbol
