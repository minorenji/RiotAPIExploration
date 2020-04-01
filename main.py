import api_object
from summoner import Summoner

if __name__ == "__main__":
    watcher = api_object.get_watcher()
    mintyorange = Summoner(watcher, 'mintyorange', 'na1')
    mintyorange.get_match_history()