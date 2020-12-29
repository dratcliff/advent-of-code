import utils


def run(entries):
    ai = {}
    all_ingredients = set()
    has_allergens = set()
    ing_occurs = {}

    for e in entries:
        ingredients = e[0].split(" ")
        ingredients = set(ingredients)
        for i in ingredients:
            if i not in ing_occurs:
                ing_occurs[i] = 1
            else:
                ing_occurs[i] += 1
            all_ingredients.add(i)
        allergens = e[1].replace(")", "")
        allergens = allergens.split(",")
        allergens = [e.lstrip(" ") for e in allergens]

        for a in allergens:
            if a not in ai:
                ai[a] = []
            ai[a].append(ingredients)

    ai2 = {}

    for each in ai:
        w = ai[each][0]
        for i in range(1, len(ai[each])):
            w = w & ai[each][i]
        for y in w:
            has_allergens.add(y)
        ai2[each] = w

    canonical = []

    done = False
    while not done:
        done = True
        for k, v in ai2.items():
            if len(v) == 1:
                for u in v:
                    for n, x in ai2.items():
                        if n != k:
                            if u in x:
                                x.remove(u)
            else:
                done = False

    for k, v in ai2.items():
        if len(v) != 1:
            raise Exception("OMG")
        for each in v:
            canonical.append((k, each))

    canonical = sorted(canonical, key=lambda x: x[0])
    canonical = [x[1] for x in canonical]

    for has_a in has_allergens:
        if has_a in all_ingredients:
            all_ingredients.remove(has_a)

    ct = 0
    for i in all_ingredients:
        ct += ing_occurs[i]

    canonical_string = ','.join(canonical)
    return (ct, canonical_string)


def test_day_twenty_one():
    entries = utils.file_to_string_list("Day21sample.txt")
    entries = [e.split(" (contains ") for e in entries]
    answer = run(entries)
    assert answer[0] == 5
    assert answer[1] == "mxmxvkd,sqjhc,fvjkl"


def day_twenty_one():
    entries = utils.file_to_string_list("Day21.txt")
    entries = [e.split(" (contains ") for e in entries]
    answer = run(entries)
    assert answer[0] == 1977
    assert answer[1] == "dpkvsdk,xmmpt,cxjqxbt,drbq,zmzq,mnrjrf,kjgl,rkcpxs"


if __name__ == "__main__":
    test_day_twenty_one()
    day_twenty_one()
