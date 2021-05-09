def flatten_dict(dictionary: dict, seperator: str, parent_key: str = None):
    result = []
    for key, value in dictionary.items():
        new_key = seperator.join(item for item in [parent_key, key] if item)
        if isinstance(value, dict):
            result.extend(flatten_dict(value, seperator, parent_key=new_key).items())
        else:
            result.append((new_key, value))
    return dict(result)
