def process_input(data):
    passports = [{}]
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            passports.append({})
            continue
        passports[-1].update(dict(map(lambda x: x.split(":"), line.split(" "))))
    return passports


def is_valid_field(field, entry):
    if field == "byr":
        return 1920 <= int(entry) <= 2002
    elif field == "iyr":
        return 2010 <= int(entry) <= 2020
    elif field == "eyr":
        return 2020 <= int(entry) <= 2030
    elif field == "hgt":
        value, unit = entry[:-2], entry[-2:]
        if unit == "cm":
            return 150 <= int(value) <= 193
        elif unit == "in":
            return 59 <= int(value) <= 76
        else:
            return False
    elif field == "hcl":
        prefix, value = entry[:1], entry[1:]
        if prefix != "#":
            return False
        try:
            int(value, 16)
        except ValueError:
            return False
        return True
    elif field == "ecl":
        return entry in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    elif field == "pid":
        if len(entry) < 9:
            return False
        return str(int(entry)).zfill(9) == entry
    elif field == "cid":
        return True
    else:
        return False


def is_valid(
    passport,
    valid_keys=set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]),
    check_fields=False,
):
    result = all(valid_key in passport.keys() for valid_key in valid_keys)
    if check_fields:
        result &= all(is_valid_field(field, entry) for field, entry in passport.items())
    return result


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
    )
    assert len(test_vals) == 4
    assert is_valid(test_vals[0])
    assert not is_valid(test_vals[1])
    assert is_valid(test_vals[2])
    assert not is_valid(test_vals[3])

    assert sum(is_valid(x) for x in test_vals) == 2

    puz = Puzzle(2020, 4)

    data = process_input(puz.input_data)

    puz.answer_a = sum(is_valid(x) for x in data)
    print(f"Part 1: {puz.answer_a}")

    assert is_valid_field("byr", "2002")
    assert not is_valid_field("byr", "2003")
    assert is_valid_field("hgt", "60in")
    assert is_valid_field("hgt", "190cm")
    assert not is_valid_field("hgt", "190in")
    assert not is_valid_field("hgt", "190")
    assert is_valid_field("hcl", "#123abc")
    assert not is_valid_field("hcl", "#123abz")
    assert not is_valid_field("hcl", "123abc")
    assert is_valid_field("ecl", "brn")
    assert not is_valid_field("ecl", "wat")
    assert is_valid_field("pid", "000000001")
    assert not is_valid_field("pid", "0123456789")

    invalid_passports = process_input(
        """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
    )

    assert sum(is_valid(x, check_fields=True) for x in invalid_passports) == 0

    valid_passports = process_input(
        """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
    )

    assert sum(is_valid(x, check_fields=True) for x in valid_passports) == 4

    puz.answer_b = sum(is_valid(x, check_fields=True) for x in data)
    print(f"Part 2: {puz.answer_b}")
