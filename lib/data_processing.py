"""
Data processing functions shared across projects.
"""

def filter_data(data, condition_func):
    """Filter a list based on a condition function"""
    return [item for item in data if condition_func(item)]

def transform_dict(data_dict, transform_func):
    """Apply a transformation function to all values in a dictionary"""
    return {key: transform_func(value) for key, value in data_dict.items()}

def group_by(items, key_func):
    """Group items by a key function"""
    result = {}
    for item in items:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result
