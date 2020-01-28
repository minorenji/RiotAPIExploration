import json
import os
import requests


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


# Contains functions to open and write to files
class FileAccess():
    @staticmethod
    def read(filepath):
        if not os.path.exists(filepath):
            print(Colors.FAIL + "Filepath \"{}\" does not exist.".format(filepath))
            return None
        with open(filepath, 'r') as file:
            if ".json" in filepath:
                return json.load(file)
            elif ".txt" in filepath:
                return file.readline()
            else:
                raise ValueError("Unknown file type or missing file extension.")

    @staticmethod
    def write(content, filepath):
        if "/" in filepath:
            FileAccess.makedir(filepath)
        with open(filepath, 'w') as outfile:
            if ".json" in filepath:
                json.dump(content, outfile)
            elif ".txt" in filepath:
                outfile.write(content)
            else:
                raise ValueError("Unknown file type or missing file extension.")

    @staticmethod
    def makedir(path):
        full_path = path.split("/")
        for i in range(1, len(full_path) + 1):
            if not os.path.exists("/".join(full_path[:i])):
                os.mkdir("/".join(full_path[:i]))


class References:
    regions = ["RU", "KR", "BR1", "OC1", "JP1", "NA1", "EUN1", "EUW1", "TR1", "LA1", "LA2"]
    patch_r = requests.get("https://raw.githubusercontent.com/CommunityDragon/Data/master/patches.json")
    FileAccess.makedir("References")
    with open('References/patches.json', 'wb') as f:
        f.write(patch_r.content)