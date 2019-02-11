import json
import os
'''
final param in create_json append - 
> 100: "taken and bonus points"
>   0: "taken"
<   0: "missed"
'''


class JsonCreator:
    def __init__(self, filename, input):
        self.input = input
        self.filename = filename

    def create_json(self, export_path):
        json_to_write = {
            "row": self.input.rows,
            "column": self.input.cols,
            "rides": []
        }

        print("here")
        for ride in self.input.rides:
                json_to_write["rides"].append([ride.start.row, ride.start.col, ride.end.row, ride.end.col, ride.json_result])

        path = os.path.join(export_path, self.filename + ".json")
        print("JsonCreator path is {0}".format(path))
        with open(path, 'w') as f:
            json.dump(json_to_write, f)
