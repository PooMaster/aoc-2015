"""
### Part 1:

--- Day 5: Doesn't He Have Intern-Elves For This? ---

Santa needs help figuring out which strings in his text file are naughty or
nice.

A **nice string** is one with all of the following properties:

    It contains at least three vowels (`aeiou` only), like `aei`, `xazegov`, or
    `aeiouaeiouaeiou`. It contains at least one letter that appears twice in a
    row, like `xx`, `abcdde` (`dd`), or `aabbccdd` (`aa`, `bb`, `cc`, or `dd`).
    It does **not** contain the strings `ab`, `cd`, `pq`, or `xy`, even if they
    are part of one of the other requirements.
"""


import re


def test_part1() -> None:
    """For example:"""
    # > `ugknbfddgicrmopn` is nice because it has at least three vowels
    # > (`u...i...o...`), a double letter (`...dd...`), and none of the
    # > disallowed substrings.
    assert is_nice("ugknbfddgicrmopn") is True

    # > `aaa` is nice because it has at least three vowels and a double letter,
    # > even though the letters used by different rules overlap.
    assert is_nice("aaa") is True

    # > `jchzalrnumimnmhp` is naughty because it has no double letter.
    assert is_nice("jchzalrnumimnmhp") is False

    # > `haegwjzuvuyypxyu` is naughty because it contains the string `xy`.
    assert is_nice("haegwjzuvuyypxyu") is False

    # > `dvszwmarrgswjxmb` is naughty because it contains only one vowel.
    assert is_nice("dvszwmarrgswjxmb") is False


"""
How many strings are nice?
"""

# === Part 1 Solution: ===


def letter_count(characters: str, test_string: str) -> int:
    """
    Returns the number of times one of the given characters is in the given test
    string.

        >>> letter_count("aeiou", "abcdde")
        2
    """
    return sum(test_string.count(char) for char in characters)


def is_nice(test_string: str) -> bool:
    """Returns True iff the input string is nice per the problem rules."""
    return all(
        [
            # It contains at least three vowels.
            letter_count("aeiou", test_string) >= 3,
            # It contains at least one letter that appears twice in a row.
            re.search(r"(\w)\1", test_string) is not None,
            # It does **not** contain the strings `ab`, `cd`, `pq`, or `xy`.
            not any(bad_str in test_string for bad_str in ["ab", "cd", "pq", "xy"]),
        ]
    )


def part1(input: str) -> int:
    """Return the number of nice lines in the given multiline string"""
    return sum(is_nice(line) for line in input.splitlines())


"""
### Part 2:

--- Part Two ---

Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a **nice string** is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the string without overlapping, like `xyxy` (`xy`) or `aabcdefgaa` (`aa`), but not like `aaa` (`aa`, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like `xyx`, `abcdefeghi` (`efe`), or even `aaa`.
"""


def test_part2() -> None:
    """For example:"""
    # > `qjhvhtzxzqqjkmpb` is nice because is has a pair that appears twice (`qj`) and a letter that repeats with exactly one letter between them (`zxz`).
    assert is_nice2("qjhvhtzxzqqjkmpb") is True

    # > `xxyxx` is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
    assert is_nice2("xxyxx") is True

    # > `uurcxstgmygtbstg` is naughty because it has a pair (`tg`) but no repeat with a single letter between them.
    assert is_nice2("uurcxstgmygtbstg") is False

    # > `ieodomkazucvgmuy` is naughty because it has a repeating letter with one between (`odo`), but no pair that appears twice.
    assert is_nice2("ieodomkazucvgmuy") is False


"""
How many strings are nice under these new rules?
"""

# === Part 2 Solution: ===


def is_nice2(test_string: str) -> bool:
    return all(
        [
            # It contains a pair of any two letters that appears at least twice in the string without overlapping
            re.search(r"(\w\w).*\1", test_string) is not None,
            # It contains at least one letter which repeats with exactly one letter between them
            re.search(r"(\w).\1", test_string) is not None,
        ]
    )


def part2(input: str) -> ...:
    """Return the number of nice lines in the given multiline string"""
    return sum(is_nice2(line) for line in input.splitlines())


if __name__ == "__main__":
    puzzle_input = open("input.txt").read()

    # Print out part 1 solution
    print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    print("Part 2:", part2(puzzle_input))
