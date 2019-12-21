from test_one import getLines

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_layers(input, height, width):
    return chunks(input, height*width)

def get_rows(layer, image_width):
    return chunks(layer, image_width)

def test_get_layers():
    layers = get_layers("123456789012", height=2, width=3)
    for layer in layers:
        print(layer)

def test_part_one():
    lines = getLines("resources/8.txt", False)
    layers = get_layers(lines[0], height=6, width=25)
    counts = []
    for layer in layers:
        counts.append((layer.count('0'), layer.count('1')*layer.count('2')))
    assert sorted(counts)[0][1] == 1848

def get_transparent_image(height, width):
    return [['2' for i in range(0, width)] for i in range(0, height)]

def decode_image(transparent_image, layers_by_row):
    img = transparent_image
    for row in layers_by_row:
        for ridx, rval in enumerate(row):
            for pidx, pval in enumerate(rval):
                if img[ridx][pidx] == '2':
                    if pval != '2':
                        img[ridx][pidx] = pval
    return img

def render(img):
    for i in img:
        print(''.join(i).replace('0', ' ').replace('1', '\u2588'))

def test_part_two():
    h = 6
    w = 25

    lines = getLines("resources/8.txt", False)
    layers = get_layers(lines[0], height=h, width=w)
    layers_by_row = []
    for layer in layers:
        rows = []
        for row in get_rows(layer, w):
            rows.append(row)
        layers_by_row.append(rows)
    
    img = get_transparent_image(height=h, width=w)
    img = decode_image(img, layers_by_row)
    render(img)

test_part_two()