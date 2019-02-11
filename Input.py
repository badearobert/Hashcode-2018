from Helper import Location


class Ride:
    def __init__(self, row_start, col_start, row_end, col_end, earliest_start, latest_finish):
        self.start = Location(row_start, col_start)
        self.end = Location(row_end, col_end)
        self.earliest_start = int(earliest_start)
        self.latest_finish = int(latest_finish)
        self.was_processed = False

    start = Location
    end = Location

    earliest_start = 0
    latest_finish = 0

    was_processed = False

    json_result = -1  # ride not taken

    def get_distance_to_finish(self):
        return Location.distance_calculator(self.start, self.end)

    def print(self):
        print("Start location: ")
        self.start.print()
        print("End location: ")
        self.end.print()
        #distance = self.get_distance()
        #print("Distance: {0}".format(distance))
        print("Earliest start: {0}".format(self.earliest_start))
        print("Latest finish: {0}".format(self.latest_finish))


class Input:
    rows = int
    cols = int
    no_of_vehicles = int
    no_of_rides = int
    bonus = int
    no_of_steps = int

    rides = []

    def __init__(self, input):
        self.rides = []
        self.rows, self.cols, self.no_of_vehicles, self.no_of_rides, self.bonus, self.no_of_steps = input[0].split()
        for item in input[1:]:
            self.rides.append(Ride(*item.split()))

    def print(self):
        print("------------------")
        print("Printing Input!")
        print("------------------")

        print('Rows: {0} | Cols {1} | Vehicles {2} | Rides {3} | Bonus {4} | Steps {5}'.format(
            self.rows, self.cols, self.no_of_vehicles, self.no_of_rides, self.bonus, self.no_of_steps))
        print("------------------")
        print("Rides: ")
        counter = 0
        for ride in self.rides:
            print("------------------")
            print("Ride {0}: ".format(counter))
            ride.print()
            counter += 1
        print("------------------")
        print("End of  Input!")
        print("------------------")

