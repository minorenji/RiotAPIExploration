from riotwatcher import RiotWatcher, ApiError
from misc import  Colors, FileAccess
import api_object


class Summoner:
    def __init__(self, watcher: RiotWatcher, name, region):
        self.name = name
        self.region = region
        self.watcher = watcher
        FileAccess.makedir("Summoners")
        self.summoner_data = None
        self.directory = "Summoners/" + self.name + "/"
        if FileAccess.makedir(self.directory):
            Colors.print_reset(Colors.OKBLUE + "Summoner file found. Updating data...")
        self.get_summoner_data()
        FileAccess.write(self.directory + "summoner_data.json", self.summoner_data)
        print(self.summoner_data)

    def get_summoner_data(self):
        try:
            self.summoner_data = self.watcher.summoner.by_name(self.region, self.name)
        except ApiError as err:
            if err.response.status_code == 401:
                Colors.print_reset(Colors.FAIL + "API key is invalid or expired.")
                self.watcher = api_object.get_watcher()
                return self.get_summoner_data()
            elif err.response.status_code == 429:
                print('Retrying in {} seconds...'.format(err.headers['Retry-After']))
                return self.get_summoner_data()
            else:
                raise