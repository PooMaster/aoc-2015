"""
--- Day 1: Not Quite Lisp ---

Santa was hoping for a white Christmas, but his weather machine's "snow"
function is powered by stars, and he's fresh out! To save Christmas, he needs
you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made available
on each day in the Advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't
find the right floor - the directions he got are a little confusing. He starts
on the ground floor (floor 0) and then follows the instructions one character at
a time.

An opening parenthesis, (, means he should go up one floor, and a closing
parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will
never find the top or bottom floors.

For example:

- (()) and ()() both result in floor 0.
- ((( and (()(()( both result in floor 3.
- ))((((( also results in floor 3.
- ()) and ))( both result in floor -1 (the first basement level).
- ))) and )())()) both result in floor -3.

To what floor do the instructions take Santa?
"""

# === My Solution ===

from typing import Optional


def part1(input: str) -> int:
    """
    For part 1, I take a very simple approach.

    Take a string composed of `(` and `)`, and return the count of `(`'s minus
    the count of `)`'s.
    """
    return input.count('(') - input.count(')')


def test_part1():
    """Check all part 1 examples."""
    assert part1("(())") == 0
    assert part1("()()") == 0
    assert part1("(((") == 3
    assert part1("(()(()(") == 3
    assert part1("))(((((") == 3
    assert part1("())") == -1
    assert part1("))(") == -1
    assert part1(")))") == -3
    assert part1(")())())") == -3


def part2(input: str) -> Optional[int]:
    """
    For part 2, I have to actually iterate through the string and keep track of
    how many parens of each type have been encountered. I think a small match
    statement fits very nicely here.

    Take a string composed of `(` and `)`, and return the index of the first
    character at which one more `)` has been encountered than `(`'s. Implicitly
    return `None` if this never occurs.
    """
    floor = 0
    for index, char in enumerate(input, start=1):
        match char:
            case '(':
                floor += 1
            case ')':
                floor -= 1
        
        if floor == -1:
            return index


def test_part2():
    """Check all part 2 examples."""
    assert part2(")") == 1
    assert part2("()())") == 5


if __name__ == "__main__":
    problem_input = open('input.txt').read()

    # Print out part 1 solution
    print(part1(problem_input))

    # Print out part 2 solution
    print(part2(problem_input))
