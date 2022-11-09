"""
### Part 1:

--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating contest year after year, you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.
"""


from enum import Enum
import itertools
import re
from typing import Iterable, NamedTuple


class Pos(NamedTuple):
    """
    This class represents a location on the problem grid.
    """

    x: int
    y: int


Grid = dict[Pos, bool]


def new_grid(size: tuple[int, int], initial_state: bool) -> Grid:
    """
    Makes and returns a new grid with the given size with all positions in the
    same initial state.
    """
    size_x, size_y = size
    return dict(
        (Pos(x, y), initial_state)
        for x, y in itertools.product(range(size_x), range(size_y))
    )


def test_part1() -> None:
    """For example:"""
    lights = new_grid((1000, 1000), False)

    assert all(not lit for lit in lights.values())

    # > `turn on 0,0 through 999,999` would turn on (or leave on) every light.
    perform_instruction("turn on 0,0 through 999,999", lights)
    assert all(lit for lit in lights.values())

    # > `toggle 0,0 through 999,0` would toggle the first line of 1000 lights,
    # > turning off the ones that were on, and turning on the ones that were
    # > off.
    perform_instruction("toggle 0,0 through 999,0", lights)
    assert all(not lights[Pos(x, 0)] for x in range(1000))

    # > `turn off 499,499 through 500,500` would turn off (or leave off) the
    # > middle four lights.
    perform_instruction("turn off 499,499 through 500,500", lights)
    assert all(
        [
            not lights[Pos(499, 499)],
            not lights[Pos(499, 500)],
            not lights[Pos(500, 499)],
            not lights[Pos(500, 500)],
        ]
    )


"""
After following the instructions, how many lights are lit?
"""

# === Part 1 Solution: ===


class InstructionKind(Enum):
    on = "turn on"
    off = "turn off"
    toggle = "toggle"


class Instruction(NamedTuple):
    kind: InstructionKind
    x_range: Iterable[int]
    y_range: Iterable[int]


instruction_pattern = re.compile(
    r"(?P<kind>[\w ]+) (?P<point1>\d+,\d+) through (?P<point2>\d+,\d+)"
)


def parse_instruction(instruction_string: str) -> Instruction:
    """
    Parse an instruction string into a named tuple.

        >>> parse_instruction("turn on 0,0 through 999,999")
        Instruction(kind=<InstructionKind.on: 'turn on'>, x_range=range(0, 1000), y_range=range(0, 1000))
    """
    m = instruction_pattern.fullmatch(instruction_string)
    if not m:
        raise ValueError(r"Could not parse instruction '{instruction_string}'")

    x1, y1 = m.group("point1").split(",")
    x2, y2 = m.group("point2").split(",")

    min_x, max_x = sorted([int(x1), int(x2)])
    min_y, max_y = sorted([int(y1), int(y2)])

    return Instruction(
        kind=InstructionKind(m.group("kind")),
        x_range=range(min_x, max_x + 1),
        y_range=range(min_y, max_y + 1),
    )


def perform_instruction(instruction_string: str, grid: Grid) -> None:
    """
    Follow the instruction to modify the grid in place.
    """
    instruction = parse_instruction(instruction_string)

    positions = map(
        Pos._make, itertools.product(instruction.x_range, instruction.y_range)
    )

    match instruction.kind:
        case InstructionKind.on:
            for pos in positions:
                grid[pos] = True

        case InstructionKind.off:
            for pos in positions:
                grid[pos] = False

        case InstructionKind.toggle:
            for pos in positions:
                grid[pos] = not grid[pos]


def part1(input: str) -> int:
    """
    Perform each line of input as an instruction on a 1000 by 1000 grid of
    lights and return the number of lights lits at the end.
    """

    lights = new_grid((1000, 1000), False)
    instructions = input.splitlines()

    for instruction in instructions:
        perform_instruction(instruction, lights)

    return sum(lights.values())


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
