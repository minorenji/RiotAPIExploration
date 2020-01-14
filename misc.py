import json
import os




# Text formatting headers
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_reset(text):
        print(text + Colors.ENDC)


class References:
    regions = ["RU", "KR", "BR1", "OC1", "JP1", "NA1", "EUN1", "EUW1", "TR1", "LA1", "LA2"]
    patch = {
        "10.1": 1578441600000
    }


# Contains functions to open and write to files
class FileAccess:
    @staticmethod
    def read(filepath):
        if not os.path.exists(filepath):
            print(Colors.FAIL + "Filepath \"{}\" does not exist.".format(filepath))
            return None
        if ".json" in filepath:
            with open(filepath, 'r') as json_file:
                return json.load(json_file)
        elif ".txt" in filepath:
            with open(filepath, 'r') as txt_file:
                return txt_file.readline()
        else:
            raise ValueError("Unknown file type or missing file extension.")

    @staticmethod
    def write(filepath, contents):
        if ".json" in filepath:
            with open(filepath, 'w') as outfile:
                json.dump(contents, outfile)
        elif ".txt" in filepath:
            with open(filepath, 'w') as outfile:
                outfile.write(contents)
        else:
            raise ValueError("Unknown file type or missing file extension.")

    @staticmethod
    def makedir(filepath):
        if os.path.exists(filepath):
            return True
        else:
            os.mkdir(filepath)