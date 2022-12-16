def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()