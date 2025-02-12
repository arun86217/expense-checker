def format_indian_currency(amount):
    """
    Format amount in Indian currency format (₹1,23,456.00)
    """
    try:
        # Convert to string and split decimal part
        str_amount = f"{float(amount):,.2f}"
        parts = str_amount.split('.')
        
        # Format the integer part in Indian system
        integer_part = parts[0].replace(',', '')
        n = len(integer_part)
        
        # Add commas for Indian number system
        if n <= 3:
            formatted = integer_part
        else:
            # First comma after 3 digits from right, then every 2 digits
            formatted = integer_part[-3:]
            integer_part = integer_part[:-3]
            while integer_part:
                formatted = integer_part[-2:] + ',' + formatted if integer_part[-2:] else integer_part[-1] + ',' + formatted
                integer_part = integer_part[:-2]
        
        # Add decimal part and rupee symbol
        return f"₹{formatted}.{parts[1]}"
    except:
        return f"₹{amount}" 