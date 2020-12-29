import utils.utils as utils

"""
For the terrible version I originally used when submitting my answers,
see Day16_original.py.
"""


def get_invalid_field_values(fields, nearby_tickets):
    valid_field_values = set()
    all_invalid = []
    
    fields = [f.split(" ") for f in fields]
    fields = [[f[1], f[3]] for f in fields]
    fields = [f for field in fields for f in field] 
    
    for g in fields:
        g = g.split("-")
        for i in range(int(g[0]), int(g[1])+1):
            valid_field_values.add(i)

    for t in nearby_tickets:
        t = t.split(",")
        for i, v in enumerate(t):
            if int(v) not in valid_field_values:
                all_invalid.append(int(v))

    return all_invalid


def calculate_field_indexes(fields, nearby_tickets):
    valid_values_by_field = {}
    all_valid_field_values = set()
    maybe_valid_tickets = []

    for f in fields:
        f = f.split(" ")
        field_name = f[0]
        f = [f[1], f[3]]

        field_name = field_name.replace(":", "")
        valid_for_field = set()
        for g in f:
            g = g.split("-")
            for i in range(int(g[0]), int(g[1])+1):
                valid_for_field.add(i)
                all_valid_field_values.add(i)
        valid_values_by_field[field_name] = valid_for_field

    for g in nearby_tickets:
        g = g.split(",")
        valid = True
        for i, h in enumerate(g):
            if int(h) not in all_valid_field_values:
                valid = False
        if valid:
            maybe_valid_tickets.append(g)

    nearby_values_by_field = {}

    for m in maybe_valid_tickets:
        for i, v in enumerate(m):
            if i not in nearby_values_by_field:
                nearby_values_by_field[i] = set()
            nearby_values_by_field[i].add(int(v))

    possible_fields_by_index = {}

    for k, v in nearby_values_by_field.items():
        for k1, v1 in valid_values_by_field.items():
            if v < v1:
                if k not in possible_fields_by_index:
                    possible_fields_by_index[k] = set()
                possible_fields_by_index[k].add(k1)

    actual_fields_by_index = possible_fields_by_index

    done = False
    while not done:
        done = True
        for field_index in actual_fields_by_index:
            if len(actual_fields_by_index[field_index]) == 1:
                for fields_with_other_index in actual_fields_by_index.values():
                    if fields_with_other_index != actual_fields_by_index[field_index]:
                        sole_key_in_index = list(
                            actual_fields_by_index[field_index])[0]
                        if sole_key_in_index in fields_with_other_index:
                            fields_with_other_index.remove(sole_key_in_index)
            else:
                done = False

    return actual_fields_by_index


def day_sixteen_part_one():
    nearby_tickets = utils.file_to_string_list("Day16nearby.txt")
    fields = utils.file_to_string_list("Day16fields.txt")
    ans = sum(get_invalid_field_values(fields, nearby_tickets))
    assert 27898 == ans


def day_sixteen_part_two():
    nearby_tickets = utils.file_to_string_list("Day16nearby.txt")
    fields = utils.file_to_string_list("Day16fields.txt")
    indexes = calculate_field_indexes(fields, nearby_tickets)

    departures = []

    for k in indexes:
        for v in indexes[k]:
            if "departure" in v:
                departures.append(k)

    my_ticket = utils.file_to_string_list("Day16your.txt")[0]
    my_ticket = my_ticket.split(",")
    my_ticket = [int(m) for m in my_ticket]

    ans = 1
    for i, v in enumerate(my_ticket):
        if i in departures:
            ans *= v

    assert ans == 2766491048287


if __name__ == "__main__":
    day_sixteen_part_one()
    day_sixteen_part_two()
