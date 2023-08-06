def wrap_str(value, *, regex: bool = False) -> str:
    return f'{"r" if regex else ""}"{value}"'
