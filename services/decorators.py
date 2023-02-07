def filter_decorator_quotes(func):
    def wrapper(*args, **kwargs):
        func().filter(*args, **kwargs)
    return wrapper 

