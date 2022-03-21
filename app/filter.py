def first_error(value):
    return list(value)[0][1][0]


def format_datetime(value, fmt='%Y-%m-%d'):
    return value.strftime(fmt)
