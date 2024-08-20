def format_count(count):
    if count >= 1000:
        return f"{count // 1000}K+"
    return str(count)