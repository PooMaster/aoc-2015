"""
### Part 1:

--- Day 2: I Was Told There Would Be No Math ---

The elves are running low on wrapping paper, and so they need to submit an order
for more. They have a list of the dimensions (length `l`, width `w`, and height
`h`) of each present, and only want to order exactly as much as they need.

Fortunately, every present is a box (a perfect [right rectangular
prism](https://en.wikipedia.org/wiki/Cuboid#Rectangular_cuboid)), which makes
calculating the required wrapping paper for each gift a little easier: find the
surface area of the box, which is `2*l*w + 2*w*h + 2*h*l`. The elves also need a
little extra paper for each present: the area of the smallest side.

For example:

-   A present with dimensions `2x3x4` requires `2*6 + 2*12 + 2*8 = 52` square
    feet of wrapping paper plus 6 square feet of slack, for a total of `58`
    square feet.

-   A present with dimensions `1x1x10` requires `2*1 + 2*10 + 2*10 = 42` square
    feet of wrapping paper plus `1` square foot of slack, for a total of `43`
    square feet.

All numbers in the elves' list are in feet. How many total **square feet of
wrapping paper** should they order?
"""

# === Part 1 Solution: ===


def parse_dimensions(line: str) -> tuple[int, int, int]:
    """
    First, the input lines have to be parsed into integer dimensions.
    
    ```
    >>> parse_dimensions("2x3x4")
    (2, 3, 4)

    ```
    """
    parts = line.split('x')
    assert len(parts) == 3, f"Got dimension line that isn't three numbers: {line}"

    return tuple(map(int, parts))


def paper_area(l: int, w: int, h: int) -> int:
    """Calculate a present's surface area plus extra."""
    # Get the area of each unique side
    sides = [l*w, w*h, h*l]

    # Save the smallest side as the amount of extra paper needed
    extra = min(sides)

    # Add up the doubles of each unique side and include the extra
    return sum(2*side for side in sides) + extra


def part1(input: str) -> int:
    """
    Split the input into separate present dimension lines, calculate each of
    their wrapping paper areas, and then return the total.
    """
    return sum(paper_area(*parse_dimensions(line)) for line in input.splitlines())


def test_part1():
    """Check all part 1 examples."""
    assert part1("2x3x4") == 58
    assert part1("1x1x10") == 43


"""
### Part 2:

--- Part Two ---

The elves are also running low on ribbon. Ribbon is all the same width, so they
only have to worry about the length they need to order, which they would again
like to be exact.

The ribbon required to wrap a present is the shortest distance around its sides,
or the smallest perimeter of any one face. Each present also requires a bow made
out of ribbon as well; the feet of ribbon required for the perfect bow is equal
to the cubic feet of volume of the present. Don't ask how they tie the bow,
though; they'll never tell.

For example:

-   A present with dimensions `2x3x4` requires `2+2+3+3 = 10` feet of ribbon to
    wrap the present plus `2*3*4 = 24` feet of ribbon for the bow, for a total
    of `34` feet.
    
-   A present with dimensions `1x1x10` requires `1+1+1+1 = 4` feet
    of ribbon to wrap the present plus `1*1*10 = 10` feet of ribbon for the bow,
    for a total of `14` feet.

How many total feet of ribbon should they order?
"""

# === Part 2 Solution: ===

from heapq import nsmallest


def ribbon_length(l: int, w: int, h: int) -> int:
    """Calculate a present's required ribbon length"""

    # Find the two smallest sides for the wrapped ribbon length
    short_sides = nsmallest(2, [l, w, h])
    wrapped_length = sum(side * 2 for side in short_sides)

    # The length of ribbon needed for the bow is equal to the present's volume
    bow_length = l * w * h

    return wrapped_length + bow_length


def part2(input: str) -> ...:
    """
    Split the input into separate present dimension lines, calculate each of
    their required ribbon lengths, and then return the total.
    """
    return sum(ribbon_length(*parse_dimensions(line)) for line in input.splitlines())


def test_part2():
    """Check all part 2 examples."""
    assert part2("2x3x4") == 34
    assert part2("1x1x10") == 14


if __name__ == "__main__":
    puzzle_input = open('input.txt').read()

    # Print out part 1 solution
    print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    print("Part 2:", part2(puzzle_input))
