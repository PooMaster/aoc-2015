"""
### Part 1:

--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and bitwise logic
gates! Unfortunately, little Bobby is a little under the recommended age range,
and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit
signal (a number from `0` to `65535`). A signal is provided to each wire by a
gate, another wire, or some specific value. Each wire can only get a signal from
one source, but can provide its signal to multiple destinations. A gate provides
no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together:
`x AND y -> z` means to connect wires `x` and `y` to an AND gate, and then
connect its output to wire `z`.

For example:

- `123 -> x` means that the signal `123` is provided to wire `x`.

- `x AND y -> z` meansthat the bitwise AND of wire `x` and wire `y` is provided
  to wire `z`.

- `p LSHIFT 2 -> q` means that the value from wire `p` is left-shifted by `2`
  and then provided to wire `q`.

- `NOT e -> f` means that the bitwise complement of the value from wire `e` is
  provided to wire `f`.

Other possible gates include `OR` (bitwise OR) and `RSHIFT` (right-shift). If,
for some reason, you'd like to **emulate** the circuit instead, almost all
programming languages (for example, C, JavaScript, or Python) provide operators
for these gates.
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
import re


def test_part1() -> None:
    # For example, here is a simple circuit:
    simple_circuit = """\
        123 -> x
        456 -> y
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 -> g
        NOT x -> h
        NOT y -> i
    """

    # After it is run, these are the signals on the wires:
    expected_signals = {
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
        "x": 123,
        "y": 456,
    }

    assert resolve_wire_values(simple_circuit) == expected_signals


"""
In little Bobby's kit's instructions booklet (provided as your puzzle input),
what signal is ultimately provided to **wire `a`**?
"""

# === Part 1 Solution: ===

"""
### Initial Thoughts

The trickiest part of this problem that jumps out at me immediately is the fact
that these wire and gate descriptions can come in any order. Since gates can't
be resolved until the values of the input wires are known, it is possible for
gates to be listed in the input before it is possible to know its input wires'
values yet. This means that all gate descriptions will have to be parsed out
beforehand and then resolved in the appropriate order.

This circuit resolution algorithm could be done in a pure brute force way, but
I'd like to find an easy way to make it faster and simpler to reason about. The
first thing to come to mind is having two sets of wires: the set that are known
about but don't have a value yet, and the set that have values already. Then,
if part of a gate's information is the set of wires that are needed as inputs,
a single set operation can be done to see if all required wires have values yet.

### Types

Now, I want to come up with some types for this code. The main three entities
in the problem description are wires, signals, and gates.
"""

# Wire names are just lowercase strings
Wire = str

# Values are integers
Value = int

# Wire values are maintained in a dictionary
WireValues = dict[Wire, Value]

# Values are 16 bit integers, so the maximum possible size is 2^16 - 1
MAX_VALUE: Value = 2**16 - 1


@dataclass(eq=True, frozen=True)
class Gate(ABC):
    """
    Gates have a set of input wires, one output wire, and a way of resolving the
    input values into the output values. Inputs can be provided as a wire name
    that needs to be resolved or as a preset static value.

    This abstract base class cannot be used directly. Subclasses must be made
    for each type of gate which implement the `resolve_ouput_value()` method.

    > This got a little nastier than I'd hoped since I needed these `Gate`
    objects to be hashable in the logic below. This required the use of frozen
    dataclasses and frozen sets. The gate objects themselves should never
    change, so that's fine. It just adds more syntactic noise.
    """

    # Note that all gates in the problem don't care about wire order, so there
    # is no need to remember the wire order.
    wire_inputs: frozenset[Wire]
    static_inputs: frozenset[Value]
    output: Wire

    @abstractmethod
    def resolve_output_value(self, *values: Value) -> Value:
        return 0


@dataclass(eq=True, frozen=True)
class ConnectionGate(Gate):
    """This represents two wires being connected"""

    def resolve_output_value(self, *values: Value) -> Value:
        (a,) = values
        return a


@dataclass(eq=True, frozen=True)
class AndGate(Gate):
    """This represents the AND gate"""

    def resolve_output_value(self, *values: Value) -> Value:
        a, b = values
        return a & b


@dataclass(eq=True, frozen=True)
class OrGate(Gate):
    """This represents the OR gate"""

    def resolve_output_value(self, *values: Value) -> Value:
        a, b = values
        return a | b


@dataclass(eq=True, frozen=True)
class LShiftGate(Gate):
    """This represents the LSHIFT gate"""

    shift_amount: int

    def resolve_output_value(self, *values: Value) -> Value:
        (a,) = values
        # Need to mask off the return value in case the value was shifted beyond
        # the 16 bit limit.
        return (a << self.shift_amount) & MAX_VALUE


@dataclass(eq=True, frozen=True)
class RShiftGate(Gate):
    """This represents the RSHIFT gate"""

    shift_amount: int

    def resolve_output_value(self, *values: Value) -> Value:
        (a,) = values
        return a >> self.shift_amount


@dataclass(eq=True, frozen=True)
class NotGate(Gate):
    """This represents the NOT gate"""

    def resolve_output_value(self, *values: Value) -> Value:
        (a,) = values
        # Bitwise NOT in Python is weird since all ints are signed with
        # arbitrary precision. Using subtraction as a workaround.
        return MAX_VALUE - a


def classify_inputs(*inputs: str) -> tuple[frozenset[Wire], frozenset[Value]]:
    """
    This parser helper function separates inputs into wire and static value
    sets.
    """
    wire_set = set()
    value_set = set()

    for input in inputs:
        if input.isdecimal():
            value_set.add(int(input))
        else:
            wire_set.add(input)

    return frozenset(wire_set), frozenset(value_set)


def parse_line(line: str) -> tuple[Wire, Value] | Gate:
    """
    This function takes in a line from the input and parses it into the
    appropriate value. All input lines are either values being assigned directly
    to wires or gate descriptions.
    """
    wire = r"[a-z]+"
    value = r"\d+"
    input = f"(?:{wire})|(?:{value})"

    # Match initial values being assigned directly to wires
    if m := re.fullmatch(rf"({value}) -> ({wire})", line):
        value, wire = m.groups()
        return (wire, int(value))

    # Match wire connections
    if m := re.fullmatch(rf"({input}) -> ({wire})", line):
        input1, output = m.groups()
        wire_inputs, static_inputs = classify_inputs(input1)
        return ConnectionGate(
            wire_inputs=wire_inputs, static_inputs=static_inputs, output=output
        )

    # Match AND gates
    if m := re.fullmatch(rf"({input}) AND ({input}) -> ({wire})", line):
        input1, input2, output = m.groups()
        wire_inputs, static_inputs = classify_inputs(input1, input2)
        return AndGate(
            wire_inputs=wire_inputs, static_inputs=static_inputs, output=output
        )

    # Match OR gates
    if m := re.fullmatch(rf"({input}) OR ({input}) -> ({wire})", line):
        input1, input2, output = m.groups()
        wire_inputs, static_inputs = classify_inputs(input1, input2)
        return OrGate(
            wire_inputs=wire_inputs, static_inputs=static_inputs, output=output
        )

    # Match LSHIFT gates
    if m := re.fullmatch(rf"({input}) LSHIFT ({value}) -> ({wire})", line):
        input1, value, output = m.groups()
        wire_inputs, static_inputs = classify_inputs(input1)
        return LShiftGate(
            wire_inputs=wire_inputs,
            static_inputs=static_inputs,
            shift_amount=int(value),
            output=output,
        )

    # Match RSHIFT gates
    if m := re.fullmatch(rf"({input}) RSHIFT ({value}) -> ({wire})", line):
        input1, value, output = m.groups()
        wire_inputs, static_inputs = classify_inputs(input1)
        return RShiftGate(
            wire_inputs=wire_inputs,
            static_inputs=static_inputs,
            shift_amount=int(value),
            output=output,
        )

    # Match NOT gates
    if m := re.fullmatch(rf"NOT ({input}) -> ({wire})", line):
        input1, output = m.groups()
        wire_inputs, static_inputs = classify_inputs(input1)
        return NotGate(
            wire_inputs=wire_inputs, static_inputs=static_inputs, output=output
        )

    raise ValueError(f"Could not parse line: '{line}'")


def resolve_wire_values(input: str) -> WireValues:
    """
    Parse the input lines into initial values and gates. Populated the wire
    value dictionary with the initial values. Then, resolve all the gates in a
    valid order while updating the wire value dictionary with the gate outputs.
    Once all gates have been resolved, return the final resulting wire value
    dictionary.
    """

    initial_values: list[tuple[Wire, Value]] = []
    unresolved_gates: set[Gate] = set()

    # Parse the input into initial values and gate descriptions
    for line in input.strip().splitlines():
        value = parse_line(line.strip())
        if isinstance(value, Gate):
            unresolved_gates.add(value)
        else:
            initial_values.append(value)

    # Create the wire value dictionary with the parsed initial values
    wire_values = dict(initial_values)

    # Keep looping until all gates are resolved
    while len(unresolved_gates) > 0:
        logging.debug(wire_values)

        # Find a gate whose input wires all have values
        for gate in unresolved_gates:
            if gate.wire_inputs.issubset(wire_values.keys()):
                break
        else:
            logging.error(wire_values)
            logging.error(unresolved_gates)
            raise ValueError("No gates found with all resolved inputs")

        logging.debug(f"Resolving gate {gate}")

        # Get the gate's resolved value
        resolved_value = gate.resolve_output_value(
            *(wire_values[wire] for wire in gate.wire_inputs), *gate.static_inputs
        )

        # Record the gate's resolved value to its output wire
        wire_values[gate.output] = resolved_value

        # Remove the gate from the unresolved list
        unresolved_gates.remove(gate)

    return wire_values


def part1(input: str) -> Value:
    wire_values = resolve_wire_values(input)
    return wire_values["a"]


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
    logging.basicConfig(level=logging.INFO)

    puzzle_input = open("input.txt").read()

    # Print out part 1 solution
    print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    print("Part 2:", part2(puzzle_input))
