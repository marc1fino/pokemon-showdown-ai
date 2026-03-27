import asyncio
from agents.random_agent import RandomBot
async def main():
    player1 = RandomBot()
    player2 = RandomBot()

    await player1.battle_against(player2, n_battles=5)

    print("Completed 5 battles")
    print(f"Player 1 victories: {player1.n_won_battles}")
    print(f"Player 2 victories: {player2.n_won_battles}")


if __name__ == "__main__":
    asyncio.run(main())