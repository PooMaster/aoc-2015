"""
### Part 1:

--- Day 8: Matchsticks ---

Space on the sleigh is limited this year, and so Santa will be bringing his list
as a digital copy. He needs to know how much space it will take up when stored.

It is common in many programming languages to provide a way to escape special
characters in strings. For example, C, JavaScript, Perl, Python, and even PHP
handle special characters in very similar ways.

However, it is important to realize the difference between the number of
characters **in the code representation of the string literal** and the number
of characters **in the in-memory string itself**.
"""


import re


def test_part1() -> None:
    """For example:"""

    # > `""` is `2` characters of code (the two double quotes), but the string
    # > contains zero characters.
    example1 = '""'
    assert len(example1) == 2
    assert character_count(example1) == 0

    # > `"abc"` is `5` characters of code, but `3` characters in the string
    # > data.
    example2 = '"abc"'
    assert len(example2) == 5
    assert character_count(example2) == 3

    # > `"aaa\"aaa"` is `10` characters of code, but the string itself contains
    # > six `"a"` characters and a single, escaped quote character, for a total
    # > of `7` characters in the string data.
    example3 = '"aaa\\"aaa"'
    assert len(example3) == 10
    assert character_count(example3) == 7

    # > `"\x27"` is `6` characters of code, but the string itself contains just
    # > one - an apostrophe (`'`), escaped using hexadecimal notation.
    example4 = '"\\x27"'
    assert len(example4) == 6
    assert character_count(example4) == 1

    example5 = '"\\\\"'
    assert len(example5) == 4
    assert character_count(example5) == 1


"""
Santa's list is a file that contains many double-quoted string literals, one on
each line. The only escape sequences used are `\\` (which represents a single
backslash), `\"` (which represents a lone double-quote character), and `\\x` plus
two hexadecimal characters (which represents a single character with that ASCII
code).

Disregarding the whitespace in the file, what is **the number of characters of
code for string literals** minus **the number of characters in memory for the
values of the strings** in total for the entire file?

For example, given the four strings above, the total number of characters of
string code (`2 + 5 + 10 + 6 = 23`) minus the total number of characters in
memory for string values (`0 + 3 + 7 + 1 = 11`) is `23 - 11 = 12`.
"""

# === Part 1 Solution: ===

"""
Immediately I want to try using regex to count how many encoding patterns are
matched in the string.
"""


def character_count(raw_string: str) -> int:
    """Return the number of characters encoded in the raw string."""

    # First, remove the beginning and end double quote.
    clipped_string = raw_string[1:-1]

    # Then match all the encoding patterns possible and return the number of
    # matches.
    return len(re.findall(r'\\x[0-9a-fA-F]{2}|\\"|\\\\|.', clipped_string))


def part1(input: str) -> int:
    """
    Split the input lines and then count up the total input string lengths and
    encoded character counts. Then return the different between the two
    """
    total_string_length = 0
    total_character_count = 0

    for raw_string in input.strip().splitlines():
        total_string_length += len(raw_string)
        total_character_count += character_count(raw_string)

    return total_string_length - total_character_count


"""
### Part 2:

--- Part Two ---

Now, let's go the other way. In addition to finding the number of characters of
code, you should now **encode each code representation as a new string** and
find the number of characters of the new encoded representation, including the
surrounding double quotes.
"""


def test_part2() -> None:
    """For example:"""

    # > `""` encodes to `"\"\""`, an increase from `2` characters to `6`.
    example1 = '""'
    assert len(example1) == 2
    assert string_repr(example1) == '"\\"\\""'
    assert len(string_repr(example1)) == 6

    # > `"abc"` encodes to `"\"abc\""`, an increase from `5` characters to `9`.
    example1 = '"abc"'
    assert len(example1) == 5
    assert string_repr(example1) == '"\\"abc\\""'
    assert len(string_repr(example1)) == 9

    # > `"aaa\"aaa"` encodes to `"\"aaa\\\"aaa\""`, an increase from `10`
    # > characters to `16`.
    example1 = '"aaa\\"aaa"'
    assert len(example1) == 10
    assert string_repr(example1) == '"\\"aaa\\\\\\"aaa\\""'
    assert len(string_repr(example1)) == 16

    # > `"\x27"` encodes to `"\"\\x27\""`, an increase from `6` characters to
    # > `11`.
    example1 = '"\\x27"'
    assert len(example1) == 6
    assert string_repr(example1) == '"\\"\\\\x27\\""'
    assert len(string_repr(example1)) == 11


"""
Your task is to find the **total number of characters to represent the newly
encoded strings** minus **the number of characters of code in each original
string literal**. For example, for the strings above, the total encoded length
(`6 + 9 + 16 + 11 = 42`) minus the characters in the original code
representation (`23`, just like in the first part of this puzzle) is `42 - 23 =
19`."""

# === Part 2 Solution: ===

"""
Again, regex calls to me.
"""


def string_repr(string: str) -> str:
    """Return the escaped representation of the given string."""

    # Put a backslash in front of any double quote or backslash characters.
    s = re.sub(r'("|\\)', r"\\\1", string)
    return '"' + s + '"'


def part2(input: str) -> int:
    """
    Split the input lines and then count up the total input string lengths and
    the total number of characters in their escaped string representations.
    Return the difference of the two
    """
    total_string_length = 0
    total_repr_length = 0

    for raw_string in input.strip().splitlines():
        total_string_length += len(raw_string)
        total_repr_length += len(string_repr(raw_string))

    return total_repr_length - total_string_length


if __name__ == "__main__":
    puzzle_input = open("input.txt").read()

    # Print out part 1 solution
    print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    print("Part 2:", part2(puzzle_input))
