# aoc-2015
Advent of Code 2015 Solutions

https://adventofcode.com/2015

I want to take the opportunity to try out following at least some of this some of [this guide on modern Python devops
processes](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/). Also, I'd like to try embedding the problem
descriptions and development notes in a literate programming style using [Pycco](https://pycco-docs.github.io/pycco/).

To test, make documentation, and run each solution, run each of these steps from inside
each day's folder.

- `poetry run python -m doctest -v *.py`
- `poetry run pytest *.py`
- `poetry run mypy .`
- `poetry run pycco *.py`
- `poetry run python main.py`
