from riotwatcher import RiotWatcher, ApiError
from misc import FileAccess
from misc import Colors


def verify_api_key(api_key):
    while True:
        watcher = RiotWatcher(api_key)
        try:
            watcher.summoner.by_name('NA1', 'mintyorange')
        except ApiError as err:
            if err.response.status_code == 401:
                Colors.print_reset(Colors.WARNING + "Invalid API key.")
                Colors.print_reset(Colors.OKBLUE + "Please enter a valid Riot API key:")
                api_key = input()
                continue
        break
    Colors.print_reset(Colors.OKGREEN + "API key verified.")
    FileAccess.write("api_key.txt", api_key)
    Colors.print_reset(Colors.OKBLUE + "RiotWatcher object created.")
    return watcher


def get_watcher():
    api_key = FileAccess.read("api_key.txt")
    if api_key is not None:
        Colors.print_reset(Colors.OKBLUE + "Using api key from file...")
    else:
        Colors.print_reset(Colors.OKBLUE + "Please enter a valid Riot API key:")
        api_key = input()
    return verify_api_key(api_key)
