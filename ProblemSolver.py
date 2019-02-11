from Helper import Location
from Input import Input, Ride
from Output import Output, Vehicle


class Solver:
    raw_input = []
    raw_output = []

    obj_in = []
    obj_out = []

    def __init__(self, raw_input, raw_output):
        self.raw_input = raw_input
        self.raw_output = raw_output

    @staticmethod
    def calculate_points(vehicle, ride, bonus):
        # if the ride was already processed, the output is not good
        if ride.was_processed:
            raise Exception("Output error: Attempting to take a ride already processed. Ride")

        # vehicle.print()
        # ride.print()

        ride_score = 0
        ride.was_processed = True

        # getting distance until the ride
        distance_to_ride = Location.distance_calculator(vehicle.position, ride.start)
        vehicle.step_time += distance_to_ride
        print("Distance until ride: {0}".format(distance_to_ride))

        # updating step time if we have to wait for earliest start, or give bonus if we arrive on time
        if vehicle.step_time < ride.earliest_start:
            print("Earliest start {0} < step time {1} , waiting for {2} duration".format(
                vehicle.step_time, ride.earliest_start, ride.earliest_start - vehicle.step_time))
            vehicle.step_time = ride.earliest_start

        # if we arrived on time or if we waited for client for earliest start: still giving bonus
        if vehicle.step_time == ride.earliest_start:
            ride_score += bonus
            ride.json_result = 1000
            print("Bonus received for this ride! + {0}".format(bonus))
        else:
            ride.json_result = 1

        # getting ride distance (from start to end)
        ride_distance = Location.distance_calculator(ride.start, ride.end)
        vehicle.step_time += ride_distance
        print("Moving {0} distance".format(ride_distance))

        # no money / bonus if we go over the finish time
        if vehicle.step_time >= int(ride.latest_finish):
            ride_score = 0
            ride.json_result = 0
            print("Ride score set to 0, time {0} > finish {1}".format(vehicle.step_time, ride.latest_finish))
        else:
            ride_score += ride_distance
            print("Received money ! {0}".format(ride_score))

        # updating vehicle location to be in the finish position
        vehicle.position = ride.end

        return ride_score

    def get_points(self):
        final_score = 0
        try:
            print("Raw input: " + str(self.raw_input))
            print("Raw output: " + str(self.raw_output))
            self.obj_in = Input(self.raw_input)
            self.obj_out = Output(self.raw_output)
            #self.obj_in.print()
            #self.obj_out.print()
            print("==================================================")
            for vehicle in self.obj_out.vehicles:
                print("----------------------------------------------")
                print("Calculating score for vehicle: {0}".format(vehicle.index))

                for ride_index in vehicle.rides_indexes:
                    ride = self.obj_in.rides[int(ride_index)]
                    print("Taking ride {0}".format(ride_index))
                    ride_score = self.calculate_points(vehicle, ride, int(self.obj_in.bonus))
                    print("Adding {0} to the total score of {1}".format(ride_score, final_score))
                    final_score += ride_score

                    print("Current step time {0}".format(vehicle.step_time))
                    print("------")

        except Exception as e:
            print("Something crashed: " + str(e))
            raise e

        return final_score
