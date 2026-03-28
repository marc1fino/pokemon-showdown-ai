import asyncio
from tabulate import tabulate
from poke_env import cross_evaluate
from agents.random_agent import RandomBot
from agents.maxdamage_agent import MaxDamageBot

async def main():
    player1 = MaxDamageBot()
    player2 = RandomBot()
    players = [player1, player2]

    results = int(input("Choose way to show results. 1: Table / 2: Print: "))
    if results == 2:
        await player1.battle_against(player2, n_battles=10)

        print("Completed 10 battles")
        print(f"Player {player1.username} victories: {player1.n_won_battles}")
        print(f"Player {player2.username} victories: {player2.n_won_battles}")

    elif results == 1:
        cross_evaluation = await cross_evaluate(players, n_challenges=10)
        table = [["-"] + [p.username for p in players]]
        for p_1, results in cross_evaluation.items():
            table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])
        
        print("Completed 10 battles")
        print(tabulate(table))



if __name__ == "__main__":
    asyncio.run(main())