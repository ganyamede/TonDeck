def format_number(number):
    """we get the shortened format of the number"""
    number = float(number)
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.3g} млрд"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.3g}м"
    elif number >= 1_000:
        return f"{number / 1_000:.3g}к"
    else:
        return str(number)