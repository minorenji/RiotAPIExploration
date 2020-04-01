from riotwatcher import RiotWatcher, ApiError
from misc import Colors, FileAccess, References
import api_object


# A summoner class to retrieve relevant stats
class Summoner:
    def __init__(self, watcher: RiotWatcher, name, region):
        self.name = name
        self.region = region
        self.api_key = FileAccess.read("api_key.txt")
        while self.region.upper() not in References.regions:
            Colors.print_reset(Colors.FAIL + "\"{}\" is not a valid region.".format(self.region))
            Colors.print_reset(Colors.OKBLUE + "Please enter a valid region.")
            Colors.print_reset("Valid regions include: {}".format(References.regions))
            self.region = input()
        self.watcher = watcher
        FileAccess.makedir("Summoners")
        self.summoner_data = None
        self.raw_matchlist = None
        self.account_id = None
        self.matchlist = {"matches": []}
        self.directory = "Summoners/" + self.name + "/"
        if FileAccess.makedir(self.directory):
            Colors.print_reset(Colors.OKBLUE + "Summoner file found. Updating data...")
        self.get_summoner_data()
        FileAccess.write(self.directory + "summoner_data.json", self.summoner_data)
        print(self.summoner_data)

    """
    Although the API should have been confirmed during the watcher object creation,
    it is possible that it has expired since then. This function checks for that.

    """
    def get_api(self, func, *args, **kwargs):

        self.watcher = api_object.verify_api_key(self.api_key)
        self.api_key = FileAccess.read("api_key.txt")
        try:
            return func(*args, **kwargs)
        except ApiError as e:
            if e.response.status_code == 429:
                print('Retrying in {} seconds...'.format(e.headers['Retry-After']))

    # Get basic summoner data
    def get_summoner_data(self):
        self.summoner_data = self.get_api(self.watcher.summoner.by_name, self.region, self.name)
        self.account_id = self.summoner_data['accountId']

    # Get all matches played by this summoner since a patch
    def get_match_history(self, last_patch=None):
        if not last_patch:
            begin_time = References.patch[sorted(References.patch.keys())[-1]]
        elif last_patch not in References.patch.keys():
            raise ValueError("Invalid patch number.")
        else:
            begin_time = References.patch[last_patch]
        self.raw_matchlist = self.get_api(self.watcher.match.matchlist_by_account, self.region, self.account_id,
                                          begin_time=begin_time, queue=420)
        FileAccess.write(self.directory + "raw_matchlist.json", self.raw_matchlist)
        match_gen = (match for match in self.raw_matchlist['matches'])
        while True:
            try:
                match = next(match_gen)
                Colors.print_reset(Colors.OKBLUE + "Recording match " + str(match['gameId']) + " ...")
                self.matchlist['matches'].append(self.get_api(self.watcher.match.by_id, self.region, match['gameId']))
            except StopIteration as e:
                break
        FileAccess.write(self.directory + "matchlist.json", self.matchlist)