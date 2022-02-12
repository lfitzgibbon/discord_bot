def remove_none_values(input: dict) -> dict:
    ''' Removes all keys whose values are None '''
    return {k: v for k, v in input.items() if v is not None}
