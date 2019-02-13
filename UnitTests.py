#!usr/bin/python

import unittest
import random
import requests
import os
from Helper import Location
from Input import Ride
from Output import Vehicle
from threading import Thread
from time import sleep

DEFAULT_NUMBER_OF_TRIES = 10000
DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 1000
DEFAULT_BONUS = 2
DEFAULT_MULTI_FACTOR_FINISH = 3

WEBPAGE_URL = 'INSERT_HERE'

project_dir = os.path.dirname(os.path.abspath(__file__))
test_file_name = os.path.join(project_dir, "out", "examples", "a_example.out")


def rnd(min=DEFAULT_MIN_VALUE, max=DEFAULT_MAX_VALUE):
    return random.randrange(min, max+1)


def generate_ride(min=DEFAULT_MIN_VALUE, max=DEFAULT_MAX_VALUE):
    new_ride = Ride(rnd(min, max), rnd(min, max), rnd(min, max), rnd(min, max), rnd(min, max), rnd(min, max * DEFAULT_MULTI_FACTOR_FINISH))
    return new_ride


def generate_ride_big_distance(min=DEFAULT_MIN_VALUE, max=DEFAULT_MAX_VALUE):
    new_ride = Ride(rnd(0, min), rnd(0, min), rnd(0, max), rnd(0, max), rnd(min, max), rnd(min, max * DEFAULT_MULTI_FACTOR_FINISH))
    return new_ride

def generate_vehicle(min=DEFAULT_MIN_VALUE, max=DEFAULT_MAX_VALUE):
    new_vehicle = Vehicle(1, 0)
    new_vehicle.position = Location(rnd(min, max), rnd(min, max))
    return new_vehicle


class Test(unittest.TestCase):

    def execute_post(self, url, cookies, payload):
        # files = {'file': ('a_example.out', payload, 'multipart/form-data')}
        files = {'file[]': payload}
        # print("Uploading file {0}".format(test_file_name))
        r = requests.post(url, files=files, cookies=cookies)

        string_to_search_for = "Uploaded files - Results"
        # print(r.text)
        self.assertNotEqual(r.text.find(string_to_search_for), -1, "Could not find uploaded files - results")

    def post_on_threads(self, number_of_threads, url, cookies, payload):
        threads = []
        for i in range(number_of_threads):
            thread = Thread(target=self.execute_post, args=(url, cookies, payload))
            thread.start()
            threads.append(thread)

        for i in threads:
            i.join()

    def the_real_tester(self, vehicle, ride, bonus):
        # data before calculation takes place
        vehicle.print()
        ride.print()

        print("Bonus: {0}".format(bonus))
        vehicle_position_before_ride = vehicle.position
        vehicle_step_time_before_ride = vehicle.step_time

        score = Solver.calculate_points(vehicle, ride, bonus)

        self.assertEqual(vehicle.position, ride.end, "The position of the vehicle is not at the end of the ride")
        self.assertEqual(ride.was_processed, True, "The ride should have been processed")

        step_time_total = vehicle_step_time_before_ride
        distance_to_car = Location.distance_calculator(vehicle_position_before_ride, ride.start)
        distance_to_car = ride.earliest_start if distance_to_car < ride.earliest_start else distance_to_car

        if distance_to_car < ride.earliest_start:
            step_time_total += ride.earliest_start
        else:
            step_time_total += distance_to_car

        distance_to_destination = Location.distance_calculator(ride.start, ride.end)
        step_time_total += distance_to_destination
        self.assertEqual(vehicle.step_time, step_time_total, "The step time is not the same as the calculated distance")

        if vehicle.step_time >= ride.latest_finish:
            self.assertEqual(score, 0, "Score should be 0 if the car was not taken to finish in time")
        else:
            # checking bonus
            expected_score = distance_to_destination
            if vehicle_step_time_before_ride + distance_to_car <= ride.earliest_start:
                expected_score += bonus
            self.assertEqual(expected_score, score, "The scores are not calculated properly!")

    def test_basic(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_basic: Iteration {0}".format(num))
            self.the_real_tester(generate_vehicle(), generate_ride(), rnd(1, 10))

    def test_big_bonus(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_big_bonus: Iteration {0}".format(num))
            self.the_real_tester(generate_vehicle(), generate_ride(), rnd(100, 1000))

    def test_big_bonus_small_distances(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_big_bonus_small_distances: Iteration {0}".format(num))
            ride = generate_ride(0, 50)
            ride.latest_finish = rnd(100, 350)
            self.the_real_tester(generate_vehicle(0, 50), ride, rnd(100, 1000))

    def test_small_distances(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_small_distances: Iteration {0}".format(num))
            ride = generate_ride(0, 50)
            ride.latest_finish = rnd(100, 350)
            self.the_real_tester(generate_vehicle(0, 50), ride, rnd(1, 10))

    def test_big_distances(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_big_distances: Iteration {0}".format(num))
            self.the_real_tester(generate_vehicle(), generate_ride_big_distance(), rnd(1, 10))

    def test_big_wait_times(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_big_wait_times: Iteration {0}".format(num))
            vehicle = generate_vehicle(0, 50)
            ride = generate_ride(0, 50)
            ride.earliest_start = rnd(100, 500)
            ride.latest_finish = 99999
            self.the_real_tester(vehicle, ride, rnd(1, 10))

    def test_big_wait_times_big_bonuses(self):
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            print("------------------------------------------")
            print("test_big_wait_times_big_bonuses: Iteration {0}".format(num))
            vehicle = generate_vehicle(0, 50)
            ride = generate_ride(0, 50)
            ride.earliest_start = rnd(100, 500)
            ride.latest_finish = 99999
            self.the_real_tester(vehicle, ride, rnd(100, 1000))

    def test_server(self):
        cookies = dict(password='')
        payload = open(test_file_name, 'rb')

        # get page
        # r = requests.get(WEBPAGE_URL, cookies=cookies)

        # post file
        for num in range(0, DEFAULT_NUMBER_OF_TRIES):
            self.post_on_threads(4, WEBPAGE_URL, cookies, payload)
            # sleep(2)

        payload.close()


if __name__ == '__main__':
    unittest.main()