from dataclasses import dataclass


def extract_name(name: str) -> tuple[str, str]:
    prefixes = {"de", "del", "De", "Del"}
    two_word_prefix = {"de la", "De La", "de La", "De la"}
    first_split = name.split(maxsplit=1)
    possible_name = first_split[0]
    if len(first_split) == 1:
        return possible_name, ""
    left = first_split[1]
    if possible_name in prefixes:
        second_split = left.split(maxsplit=1)
        possible_name = possible_name + " " + second_split[0]
        left = second_split[1]
        if possible_name in two_word_prefix:
            third_split = left.split(maxsplit=1)
            name = possible_name + " " + third_split[0]
            left = third_split[1]
        else:
            name = possible_name
    else:
        name = possible_name
    # if the leftover starts with de or del or de la, it is part of this last name
    left_split = left.split()
    if left_split[0] in prefixes:
        if left_split[0] + " " + left_split[1] in two_word_prefix:
            # append to the name
            name += " " + left_split[0] +" " + left_split[1] + " " + left_split[2]
            left = " ".join(left_split[3:])
        else:
            # append to name
            name += " " + left_split[0] + " " + left_split[1]
            left = " ".join(left_split[2:])
    return name, left


@dataclass
class Name:
    first_family_name: str
    second_family_name: str
    widow_family_name: str
    given_names: list[str]

def extract_widow_name(name:str) -> tuple[str, str]:
    assert name.lower().startswith("vda ")
    name = name[4:]
    family_name, left = extract_name(name)
    return family_name, left


def process_name(name) -> Name:
    # special cases
    # de 
    # del 
    widow_family_name = None
    second_family_name = None
    first_family_name, left  = extract_name(name)
    if left.lower().startswith("vda "):
        widow_family_name, left = extract_widow_name(left)
    else: 
        second_family_name, left = extract_name(left)
        # sometimes there is a third last name with vda
        if left.lower().startswith("vda "):
            widow_family_name, left = extract_widow_name(left)

    given_names = []
    while left != "":
        name, left = extract_name(left)
        given_names.append(name)
    if len(given_names) == 0:
        # we assume there is no second last name and use it as first
        given_names.append(second_family_name)
        second_family_name = ""
    return Name(first_family_name=first_family_name, second_family_name=second_family_name, widow_family_name=widow_family_name, given_names=given_names)


with open("names.txt") as f:
    for line in f:
        line = line.strip()

        name = process_name(line)
        print (f"{line}=>l1 {name.first_family_name} |l2 {name.second_family_name} |lw {name.widow_family_name} |f {';'.join(name.given_names)}")








