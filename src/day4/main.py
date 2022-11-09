"""
### Part 1:

--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as
gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
least **five zeroes**. The input to the MD5 hash is some secret key (your puzzle
input, given below) followed by a number in decimal. To mine AdventCoins, you
must find Santa the lowest positive number (no leading zeroes: `1`, `2`, `3`, ...)
that produces such a hash.
"""


import hashlib
import itertools


def test_part1() -> None:
    """For example:"""
    # > If your secret key is `abcdef`, the answer is `609043`, because the MD5
    # > hash of `abcdef609043` starts with five zeroes (`000001dbbfa...`), and
    # > it is the lowest such number to do so.
    assert part1("abcdef") == 609043

    # > If your secret key is `pqrstuv`, the lowest number it combines with to
    # > make an MD5 hash starting with five zeroes is `1048970`; that is, the
    # > MD5 hash of `pqrstuv1048970` looks like `000006136ef...`.
    assert part1("pqrstuv") == 1048970


# === Part 1 Solution: ===


def has_leading_zeros(zero_count: int, test_string: str) -> bool:
    return test_string.startswith("0" * zero_count)


def part1(input: str) -> int:
    """
    Append ever increasing integers to the input string until it MD5 hashes to a
    value that satisfies the problem constraint.
    """
    for index in itertools.count():
        test_string = input + str(index)
        hashed_string = hashlib.md5(test_string.encode()).hexdigest()
        if has_leading_zeros(5, hashed_string):
            return index

    return -1


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    # > `""` results in  `...`.
    assert part2("") == ...


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(input: str) -> ...:
    """ """
    return ...


if __name__ == "__main__":
    puzzle_input = open("input.txt").read()

    # Print out part 1 solution
    print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    print("Part 2:", part2(puzzle_input))
