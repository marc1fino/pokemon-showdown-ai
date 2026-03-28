from poke_env import Player, AccountConfiguration
from poke_env.ps_client import ShowdownServerConfiguration, ServerConfiguration

local_server = ServerConfiguration("ws://localhost:8000/showdown/websocket", "http://localhost:8000/action.php?")
class MaxDamageBot(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            if battle.can_tera:
                return self.create_order(best_move, terastallize=True)
            if battle.can_dynamax:
                return self.create_order(best_move, dynamax=True)
            if battle.can_mega_evolve:
                return self.create_order(best_move, mega_evolve=True)
            if battle.can_z_move:
                return self.create_order(best_move, z_move=True)

            return self.create_order(best_move)
        
        else:
            return self.choose_random_move(battle)
    battle_format="gen9randombattle",
    server_configuration=local_server,
    account_configuration=AccountConfiguration(
        username="MaxDamageBot",
        password=None,
    ),