def file_to_strings(filename):
    return [x.strip('\n') for x in open(filename).readlines()]

if __name__ == "__main__":
    print(file_to_strings("test-input.txt"))