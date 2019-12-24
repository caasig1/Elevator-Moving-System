from typing import List

import simulation
import algorithms
from simulation import Simulation
from hypothesis import given, settings
from hypothesis.strategies import integers, lists

# DON'T RUN ALL TESTS SIMULTANEOUSLY, RUN INDIVIDUAL
# Since there only one single file is being used to generate arrivals

# =========== Arrival Generation Algorithms =========== #
# Random Algorithm
# test 'total_people' = 'people_generated_per_round' * num_rounds

# num_rounds = 15


@settings(max_examples=20)
@given(integers(min_value=1, max_value=5), integers(min_value=6, max_value=10))
def test_random_algorithm_equals(gen: int, elev: int):
    arrival_gen = algorithms.RandomArrivals(6, gen)
    move_gen = algorithms.RandomAlgorithm()
    """Run a test simulation, and return the simulation statistics"""
    config = {
        'num_rounds': 15,
        'num_floors': 6,
        'num_elevators': elev,
        'elevator_capacity': 3,
        'num_people_per_round': gen,
        'arrival_generator': arrival_gen,
        # File arrival generator with 6 max floors and arrivals dictated by file
        # 'arrival_generator': arrival_gen,
        'moving_algorithm': move_gen,
        'visualize': False
    }

    sim = Simulation(config)
    stats = sim.run(15)
    people = 0
    for elevator in sim.elevators:
        people += len(elevator.passengers)
    for key in sim.waiting:
        people += len(sim.waiting[key])
    assert stats['total_people'] == gen * 15
    assert stats['total_people'] - stats['people_completed'] == people
# PASSED 10:42 16/10/18


# File Arrival Generation Algorithm
# arrivals_1 File:
# 1, 5, 1, 4, 3
# 5, 5, 1, 4, 3
# 9, 3, 5, 4, 1
# 13, 1, 6
# 14, 6, 1
@settings(max_examples=20)
@given(integers(min_value=1, max_value=20))
def test_file_arrivals_algorithm_equals(elev: int):
    #   10 is arbitrary
    gen = 10
    arrival_gen = algorithms.FileArrivals(6, 'arrival_files/arrivals_1.csv')
    move_gen = algorithms.RandomAlgorithm()
    """Run a test simulation, and return the simulation statistics"""
    config = {
        'num_rounds': 15,
        'num_floors': 6,
        'num_elevators': elev,
        'elevator_capacity': 3,
        'num_people_per_round': gen,
        'arrival_generator': arrival_gen,
        # File arrival generator with 6 max floors and arrivals dictated by file
        # 'arrival_generator': arrival_gen,
        'moving_algorithm': move_gen,
        'visualize': False
    }

    sim = Simulation(config)
    stats = sim.run(15)
    people = 0
    for elevator in sim.elevators:
        people += len(elevator.passengers)
    for key in sim.waiting:
        people += len(sim.waiting[key])
    assert stats['total_people'] == 8   # 8 according to sample_arrivals.csv
    assert stats['total_people'] - stats['people_completed'] == people
# PASSED 10:42 16/10/18


# =========== Elevator Moving Algorithms =========== #

# Pushy Passenger Algorithm
# arrivals_2 File:
# 1,3,1,3,5,3,4,5,3,5,6
# 10,4,5,3,4
# 14,1,6,6,1
def test_pushy_passenger():
    gen = 10
    arrival_gen = algorithms.FileArrivals(6, 'arrival_files/arrivals_2.csv')
    move_gen = algorithms.PushyPassenger()
    config = {
        'num_rounds': 15,
        'num_floors': 6,
        'num_elevators': 2,
        'elevator_capacity': 3,
        'num_people_per_round': gen,
        'arrival_generator': arrival_gen,
        # File arrival generator with 6 max floors and arrivals dictated by file
        # 'arrival_generator': arrival_gen,
        'moving_algorithm': move_gen,
        'visualize': False
    }
    sim = simulation.Simulation(config)
    stats = sim.run(15)
    people = 0
    for elevator in sim.elevators:
        people += len(elevator.passengers)
    for key in sim.waiting:
        people += len(sim.waiting[key])
    assert stats['num_iterations'] == 15
    assert stats['total_people'] == 9
    assert stats['people_completed'] == 7
    assert stats['max_time'] == 9
    assert stats['min_time'] == 2
    assert stats['avg_time'] == 5
    assert stats['total_people'] - stats['people_completed'] == people
# PASSED 10:42 16/10/18


# arrivals_3 ShortSighted Algorithm
# 1,3,1,3,2,3,4,5,3,5,6
# 10,4,5,2,4
# 14,1,6,6,1
def test_short_sighted():
    gen = 10
    arrival_gen = algorithms.FileArrivals(6, 'arrival_files/arrivals_3.csv')
    move_gen = algorithms.ShortSighted()
    config = {
        'num_rounds': 15,
        'num_floors': 6,
        'num_elevators': 2,
        'elevator_capacity': 3,
        'num_people_per_round': gen,
        'arrival_generator': arrival_gen,
        # File arrival generator with 6 max floors and arrivals dictated by file
        # 'arrival_generator': arrival_gen,
        'moving_algorithm': move_gen,
        'visualize': False
    }
    sim = simulation.Simulation(config)
    stats = sim.run(15)
    people = 0
    for elevator in sim.elevators:
        people += len(elevator.passengers)
    for key in sim.waiting:
        people += len(sim.waiting[key])
    assert stats['num_iterations'] == 15
    assert stats['total_people'] == 9
    assert stats['people_completed'] == 7
    assert stats['max_time'] == 8
    assert stats['min_time'] == 1
    assert stats['avg_time'] == 4
    assert stats['total_people'] - stats['people_completed'] == people
# PASSED 10:42 16/10/18


if __name__ == '__main__':
    import pytest
    pytest.main(['test_simulation.py'])
