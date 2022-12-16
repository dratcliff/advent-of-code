def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()

lines = get_data('input.txt')
lines = lines.strip().split('\n')