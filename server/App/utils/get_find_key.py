def find_key(data, key):
    """searches the entire list for the required argument"""
    if isinstance(data, dict):
        if key in data: return f"{data[key]}"
        for v in data.values():
            result = find_key(v, key)
            if result: return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, key)
            if result: return result
    return None