"""CSC148 Assignment 1 - People and Elevators

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains classes for the two "basic" entities in this simulation:
people and elevators. We have provided basic outlines of these two classes
for you; you are responsible for implementing these two classes so that they
work with the rest of the simulation.

You may NOT change any existing attributes, or the interface for any public
methods we have provided. However, you can (and should) add new attributes,
and of course you'll have to implement the methods we've provided, as well
as add your own methods to complete this assignment.

Finally, note that Person and Elevator each inherit from a kind of sprite found
in sprites.py; this is to enable their instances to be visualized properly.
You may not change sprites.py, but are responsible for reading the documentation
to understand these classes, as well as the abstract methods your classes must
implement.
"""
from __future__ import annotations
from typing import List
from sprites import PersonSprite, ElevatorSprite


class Elevator(ElevatorSprite):
    """An elevator in the elevator simulation.

    Remember to add additional documentation to this class docstring
    as you add new attributes (and representation invariants).

    === Attributes ===
    passengers: A list of the people currently on this elevator
    maximum_capacity: The total number of people allowed on an elevator
    current_floor: The floor that the elevator is currently on
    current_capacity: The number of people currently on the elevator

    === Representation invariants ===
    maximum_capacity >= 1
    current_floor <= number of floors and current_floor >= 1
    current_capacity <= maximum_capacity and current_capacity >= 0
    """
    passengers: List[Person]
    maximum_capacity: int
    current_floor: int
    current_capacity: int

    def __init__(self, elevator_capacity: int) -> None:
        """Initialize a new Elevator

        Preconditions:
            maximum_capacity >= 1
            current_floor <= number of floors and current_floor >= 1
            current_capacity <= maximum_capacity and current_capacity >= 0
        """
        self.current_floor = 1
        self.maximum_capacity = elevator_capacity
        self.current_capacity = 0
        self.passengers = []
        ElevatorSprite.__init__(self)

    def fullness(self) -> float:
        """Return how full the elevator is
        """
        return self.current_capacity / self.maximum_capacity


class Person(PersonSprite):
    """A person in the elevator simulation.

    === Attributes ===
    start: the floor this person started on
    target: the floor this person wants to go to
    wait_time: the number of rounds this person has been waiting
    total_time: the time it takes for a person to get to their target location

    === Representation invariants ===
    start >= 1
    target >= 1
    wait_time >= 0
    total_time >= 0
    """
    start: int
    target: int
    wait_time: int
    total_time: int

    def __init__(self, current_floor: int, destination: int) -> None:
        """Initialize a Person

        Preconditions:
            start >= 1
            target >= 1
            wait_time >= 0
            total_time >= 0
        """
        self.wait_time = 0
        self.start = current_floor
        self.target = destination
        self.total_time = 0
        PersonSprite.__init__(self)

    def get_anger_level(self) -> int:
        """Return this person's anger level.

        A person's anger level is based on how long they have been waiting
        before reaching their target floor.
            - Level 0: waiting 0-2 rounds
            - Level 1: waiting 3-4 rounds
            - Level 2: waiting 5-6 rounds
            - Level 3: waiting 7-8 rounds
            - Level 4: waiting >= 9 rounds
        """
        if self.start != self.target:
            self.wait_time += 1
        if self.wait_time < 3:
            return 0
        elif self.wait_time < 5:
            return 1
        elif self.wait_time < 7:
            return 2
        elif self.wait_time < 9:
            return 3
        else:
            return 4


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-attributes': 12,
        'disable': ['R0201'],
        'extra-imports': ['sprites'],
        'max-nested-blocks': 4
    })
