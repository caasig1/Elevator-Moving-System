"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
            (keys are floor numbers, values are the list of waiting people)
    people_per_round: the number of people who arrive each round
    results: shows the number of iterations/rounds that occurred, the number of
            people who were generated, the number of people who arrive at their
            destination, the maximum time (in rounds) for a person to
            arrive at their destination, the minimum time (in rounds) for a
            person to arrive at their destination, and the average time of all
            people who arrived at their destinations

    === Representation Invariants ===
    arrival_generator is RandomArrivals(num_floors, people_per_round) or
        FileArrivals(num_floors, 'csv_file_name')
    moving_algorithm is RandomAlgorithm() or PushyPassenger() or ShortSighted()
    num_floors >= 2
    waiting keys are floor numbers
    people_per_round >= 0
    """
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    waiting: Dict[int, List[Person]]
    people_per_round: int
    results: Dict[str, int]
    visualizer: Visualizer

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration.

        Precondition:
            arrival_generator is RandomArrivals(num_floors, people_per_round) or
                FileArrivals(num_floors, 'csv_file_name')
            moving_algorithm is RandomAlgorithm() or PushyPassenger() or
                ShortSighted()
            num_floors >= 2
            waiting keys are floor numbers
            people_per_round >= 0
        """
        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.
        self.arrival_generator = config['arrival_generator']
        self.elevators = []
        for i in range(config['num_elevators']):
            self.elevators.append(Elevator(config['elevator_capacity']))
        self.moving_algorithm = config['moving_algorithm']
        self.num_floors = config['num_floors']
        self.waiting = {}
        for i in range(1, self.num_floors + 1):
            self.waiting[i] = []
        self.people_per_round = config['num_people_per_round']
        self.results = {
            'num_iterations': 0,
            'total_people': 0,
            'people_completed': 0,
            'max_time': 0,
            'min_time': 0,
            'avg_time': 0.0}
        self.visualizer = Visualizer(self.elevators, self.num_floors,
                                     config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Pause for 1 second and add an iteration
            self.visualizer.wait(1)
            self.results['num_iterations'] += 1

        if self.results['people_completed'] == 1:
            self.results['max_time'] = self.results['min_time']
        elif self.results['people_completed'] == 0:
            self.results['max_time'] = -1
            self.results['min_time'] = -1
            self.results['avg_time'] = -1.0
        if self.results['people_completed'] != 0:
            self.results['avg_time'] = self.results['avg_time'] / (self.results[
                'people_completed'])
        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals.

        Precondition:
            round_num >= 0
        """
        arriving = self.arrival_generator.generate(round_num)
        for person in arriving:
            self.waiting[person].extend(arriving[person])
            self.results['total_people'] += len(arriving[person])
        self.visualizer.show_arrivals(arriving)

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        for elevator in self.elevators:
            i = len(elevator.passengers) - 1
            while not i < 0:
                person = elevator.passengers[i]
                if person.start == person.target:
                    elevator.current_capacity -= 1
                    self.visualizer.show_disembarking(person, elevator)
                    self.results['people_completed'] += 1
                    self.results['avg_time'] += person.total_time
                    if person.total_time < self.results['min_time'] or \
                            self.results['min_time'] == 0:
                        self.results['min_time'] = person.total_time
                    elif person.total_time > self.results['max_time'] or \
                            self.results['max_time'] == 0:
                        self.results['max_time'] = person.total_time
                    elevator.passengers.pop(i)
                i -= 1

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for elevator in self.elevators:
            if elevator.fullness() == 1:
                continue
            else:
                while elevator.fullness() != 1:
                    if len(self.waiting[elevator.current_floor]) > 0:
                        elevator.current_capacity += 1
                        self.visualizer.show_boarding(
                            self.waiting[elevator.current_floor][0], elevator)
                        elevator.passengers.append(
                            self.waiting[elevator.current_floor].pop(0))
                    else:
                        break

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        algorithm = self.moving_algorithm
        self.visualizer.show_elevator_moves(self.elevators,
                                            algorithm.move_elevators(
                                                self.elevators,
                                                self.waiting,
                                                self.num_floors))
        for elevator in self.elevators:
            for person in elevator.passengers:
                person.total_time += 1
        for floor in self.waiting:
            for person in self.waiting[floor]:
                person.total_time += 1

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        return self.results


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 5,
        'num_elevators': 2,
        'elevator_capacity': 10,
        # This is likely not used.
        'num_people_per_round': 2,
        'arrival_generator': algorithms.FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': algorithms.ShortSighted(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(10)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    print(sample_run())

    import python_ta

    python_ta.check_all(config={
        'max-attributes': 12,
        'disable': ['R0201'],
        'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
        'max-nested-blocks': 4
    })
