from poke_env import RandomPlayer, AccountConfiguration
from poke_env.ps_client import ShowdownServerConfiguration, ServerConfiguration

local_server = ServerConfiguration("ws://localhost:8000/showdown/websocket", "http://localhost:8000/action.php?")
class RandomBot(RandomPlayer):
    battle_format="gen9randombattle",
    server_configuration=local_server,
    account_configuration=AccountConfiguration(
        username="RandomBot",
        password=None,
    ),