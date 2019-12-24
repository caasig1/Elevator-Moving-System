"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

        Generate 0 people if self.num_people is None.

        For our testing purposes, this class *must* have the same initializer
        header as ArrivalGenerator. So if you choose to to override the
        initializer, make sure to keep the header the same!

        Hint: look up the 'sample' function from random.

    === Attributes ===
    people: A Dictionary that has the floor number as the keys and a List of
        people as the values
    num_floor: The number of floors int he simulation

    === Representation Invariants ===
    people keys are floor numbers
    num_floor >= 2
    """
    people: Dict[int, List[Person]]
    num_floor: int

    def __init__(self, max_floor: int, num_people: int) -> None:
        """Initialize a new Random Arrival Generator

        Preconditions:
            people keys are floor numbers
            num_floor >= 2

        """
        ArrivalGenerator.__init__(self, max_floor, num_people)
        self.num_floor = max_floor
        self.people = {}

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Refer to the Parent class
        """
        for num in range(1, self.num_floor + 1):
            self.people[num] = []
        person_location = []
        person_destination = []
        if self.num_people == 0:
            return self.people
        else:
            i = 0
            while i < self.num_people:
                floors = list(range(1, self.max_floor + 1))
                location = random.sample(floors, 1)
                person_location += location
                floors.pop(floors.index(location[0]))
                destination = random.sample(floors, 1)
                person_destination += destination
                i += 1
            while len(person_location) > 0:
                cur_loc = person_location[0]
                cur_dest = person_destination[0]
                self.people[cur_loc] += [Person(cur_loc, cur_dest)]
                person_destination.pop(0)
                person_location.pop(0)
            return self.people


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.

    === Attributes ===
    file_content: The contents of the file are stored line by line into a list
    people: A Dictionary that has the floor number as the keys and a List of
        people as the values
    round_number: The round number to store when people are spawned

    === Representation Invariants ===
    people keys are floor numbers
    round_number >= 0
    """
    file_content: List[int]
    people: Dict[int, List[Person]]
    round_number: int

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
            people keys are floor numbers
            round_number >= 0
        """
        ArrivalGenerator.__init__(self, max_floor, None)
        self.round_number = 0
        self.people = {}

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        self.file_content = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if len(line) % 2 == 1:
                    self.file_content.append(line)
                else:
                    raise Exception('Incorrect number of inputs in csv file.')

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Refer to the Parent Class
        """
        for num in range(1, self.max_floor + 1):
            self.people[num] = []
        file = []
        for line in self.file_content:
            file.append(list(map(int, line)))
        for line in file:
            if line[0] == round_num:
                line.pop(0)
                for thing in line[0::2]:
                    loc = thing
                    dest = line[line.index(thing) + 1]
                    self.people[thing] = [Person(loc, dest)]
                    line.pop(0)  # remove first location
                    line.pop(0)  # remove first destination
            elif line[0] != round_num:
                continue
        return self.people


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.

        Precondition:
            waiting keys are floor numbers
            max_floor >= 2
        """
        raise NotImplementedError

    def update_elevators(self, elevator: Elevator, movement: Direction) -> None:
        """Update the location of each elevator and its passengers before it
        moves visually to the next floor.
        """
        if movement == Direction.UP:
            elevator.current_floor += 1
            for person in elevator.passengers:
                person.start += 1
        elif movement == Direction.DOWN:
            elevator.current_floor -= 1
            for person in elevator.passengers:
                person.start -= 1


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]], max_floor: int) -> \
            List[Direction]:
        """Refer to the Parent class
        """
        elev_direction = []
        for elevator in elevators:
            movement = [Direction.UP, Direction.STAY, Direction.DOWN]
            if elevator.current_floor == 1:
                movement.pop(2)
            elif elevator.current_floor == max_floor:
                movement.pop(0)
            choice = random.choice(movement)
            elev_direction.append(choice)
            self.update_elevators(elevator, choice)
        return elev_direction


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]], max_floor: int) -> \
            List[Direction]:
        """Refer to the Parent class
        """
        elev_direction = []
        for elevator in elevators:
            if len(elevator.passengers) == 0:
                lowest_floor = max_floor + 1
                for element in waiting:
                    if len(waiting[element]) != 0 and element < lowest_floor:
                        lowest_floor = element
                if lowest_floor == max_floor + 1:
                    elev_direction.append(Direction.STAY)
                    choice = Direction.STAY
                elif lowest_floor > elevator.current_floor:
                    elev_direction.append(Direction.UP)
                    choice = Direction.UP
                elif lowest_floor < elevator.current_floor:
                    elev_direction.append(Direction.DOWN)
                    choice = Direction.DOWN
            else:
                if elevator.passengers[0].target < elevator.current_floor:
                    elev_direction.append(Direction.DOWN)
                    choice = Direction.DOWN
                else:
                    elev_direction.append(Direction.UP)
                    choice = Direction.UP
            self.update_elevators(elevator, choice)
        return elev_direction


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]], max_floor: int) -> \
            List[Direction]:
        """Refer to the Parent class
        """
        elev_direction = []
        for elevator in elevators:
            if len(elevator.passengers) != 0:
                go_to = max_floor + 2
                for passenger in elevator.passengers:
                    diff = abs(passenger.target - elevator.current_floor)
                    if diff < go_to:
                        go_to = passenger.target
                if go_to < elevator.current_floor:
                    elev_direction.append(Direction.DOWN)
                    choice = Direction.DOWN
                else:
                    elev_direction.append(Direction.UP)
                    choice = Direction.UP
            else:
                floor_num, decision = max_floor + 1, max_floor + 1
                floor = 1
                while floor < max_floor + 1:
                    diff = abs(floor - elevator.current_floor)
                    if diff < decision and len(waiting[floor]) != 0:
                        decision = diff
                        floor_num = floor
                    floor += 1
                if floor_num == max_floor + 1:
                    elev_direction.append(Direction.STAY)
                    choice = Direction.STAY
                elif floor_num < elevator.current_floor:
                    elev_direction.append(Direction.DOWN)
                    choice = Direction.DOWN
                else:
                    elev_direction.append(Direction.UP)
                    choice = Direction.UP
            self.update_elevators(elevator, choice)
        return elev_direction


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta

    python_ta.check_all(config={
        'max-attributes': 12,
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201']
    })
