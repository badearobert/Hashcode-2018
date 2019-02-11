from Helper import Location

class Vehicle:
    def __init__(self, index, rides):
        self.rides_indexes = rides
        self.index = index
        self.position = Location(0, 0)

    index = int
    rides_indexes = []
    step_time = 0
    position = Location

    def print(self):
        print("Vehicle {0} has the following rides (indexes): {1}, Location {2}, {3}".format(
            self.index, self.rides_indexes, self.position.row, self.position.col))


class Output:
    def __init__(self, output):
        self.vehicles = []
        index = 0
        for lines in output:
            line_split = lines.split()
            number_of_rides = line_split[0]

            if str(number_of_rides) != str(len(line_split[1:])):
                raise Exception("Output error: Number of rides incorrect set. Line: {0} Required: {1} Found: {2}".format(
                    line_split, number_of_rides, len(line_split[1:])))

            self.vehicles.append(Vehicle(index, line_split[1:]))
            index += 1

    vehicles = []

    def print(self):
        print("------------------")
        print("Printing Output!")
        print("------------------")
        for vehicle in self.vehicles:
            vehicle.print()
        print("------------------")
        print("End of  Output!")
        print("------------------")
