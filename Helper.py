class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    row = int
    col = int

    def print(self):
        print("Row: {0}, Col: {1}".format(self.row, self.col))

    @staticmethod
    def distance_calculator(start, end):
        return int(abs(int(start.row) - int(end.row)) + abs(int(start.col) - int(end.col)))
