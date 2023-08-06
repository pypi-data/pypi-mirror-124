def print_error(error, token):
    try:
        print(
            "{} at {}:{} to {}:{}".format(
                error, token.line, token.column, token.end_line, token.end_column
            )
        )
    except AttributeError:
        print("{} at {}:{}".format(error, token.line, token.column))
