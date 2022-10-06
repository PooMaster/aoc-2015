"""
### Part 1:

--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and
then an elf at the North Pole calls him via radio and tells him where to move
next. Moves are always exactly one house to the north (`^`), south (`v`), east
(`>`), or west (`<`). After each move, he delivers another present to the house
at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so
his directions are a little off, and Santa ends up visiting some houses more
than once. How many houses receive **at least one present**?
"""


import logging
from typing import Iterable, NamedTuple


def test_part1() -> None:
    """For example:"""
    # > `>` delivers presents to `2` houses: one at the starting location, and
    # > one to the east.
    assert part1(">") == 2

    # > `^>v<` delivers presents to `4` houses in a square, including twice to
    # > the house at his starting/ending location.
    assert part1("^>v<") == 4

    # > `^v^v^v^v^v` delivers a bunch of presents to some very lucky children at
    # > only `2` houses.
    assert part1("^v^v^v^v^v") == 2


# === Part 1 Solution: ===


class Pos(NamedTuple):
    """
    This class represents a location on the problem grid. The `x` coordinate
    goes positive north, negative south. The `y` coordinate goes positive east,
    negative west.
    """

    x: int
    y: int

    def move(self: "Pos", offset: "Pos") -> "Pos":
        """Return a new `Pos` moved by the given offset."""
        return Pos(self.x + offset.x, self.y + offset.y)


directions = {
    "^": Pos(1, 0),
    "v": Pos(-1, 0),
    ">": Pos(0, 1),
    "<": Pos(0, -1),
}


def follow_path(starting_position: Pos, path: str) -> Iterable[Pos]:
    """
    Iterate through the directions in the given path string and yield all
    resulting positions encountered while following the path.
    """

    current_position = starting_position
    logging.debug(f"Starting at {current_position}")
    yield current_position

    for direction in path:
        current_position = current_position.move(directions.get(direction, Pos(0, 0)))
        logging.debug(f"Moved {direction} to {current_position}")
        yield current_position


def part1(input: str) -> int:
    """
    Take the list of directions, find the path that will be taken, and return
    the number of unique positions.
    """
    starting_position = Pos(0, 0)
    unique_positions = set(follow_path(starting_position, input))
    return len(unique_positions)


"""
### Part 2:

The next year, to speed up the process, Santa creates a robot version of
himself, **Robo-Santa**, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the
same starting house), then take turns moving based on instructions from the elf,
who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive **at least one present**?
"""


def test_part2() -> None:
    """For example:"""
    # > `^v` delivers presents to `3` houses, because Santa goes north, and then
    # > Robo-Santa goes south.
    assert part2("^v") == 3

    # > `^>v<` now delivers presents to `3` houses, and Santa and Robo-Santa end
    # > up back where they started.
    assert part2("^>v<") == 3

    # > `^v^v^v^v^v` now delivers presents to `11` houses, with Santa going one
    # > direction and Robo-Santa going the other.
    assert part2("^v^v^v^v^v") == 11


# === Part 2 Solution: ===


def part2(input: str) -> int:
    """
    Slice the input directions to be every other direction starting from the
    first for Santa, and every other direction starting from the second for
    Robo-Stana. Then, combine the two sets of positions and return the total
    number of unique positions.
    """

    starting_position = Pos(0, 0)
    santa_positions = set(follow_path(starting_position, input[::2]))
    robo_santa_positions = set(follow_path(starting_position, input[1::2]))
    return len(santa_positions | robo_santa_positions)


if __name__ == "__main__":
    puzzle_input = open("input.txt").read().rstrip()

    # Print out part 1 solution
    print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    print("Part 2:", part2(puzzle_input))
