# Pokémon Showdown AI

An AI battle framework for **Pokémon Showdown** featuring rule-based agents, competitive heuristics, local bot tournaments, public ladder play, and reinforcement-learning experiments powered by PPO.

The project is built around Generation 9 Random Battles (`gen9randombattle`) and uses [`poke-env`](https://github.com/hsahovic/poke-env) to communicate with either a local Pokémon Showdown server or the official online server.

<br>

<p align="left">
  <img alt="Python" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" />&nbsp;&nbsp;
  <img alt="PyTorch" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pytorch/pytorch-original.svg" />&nbsp;&nbsp;
  <img alt="NumPy" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" />&nbsp;&nbsp;
  <img alt="Pandas" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" />&nbsp;&nbsp;
  <img alt="Matplotlib" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/matplotlib/matplotlib-original.svg" />&nbsp;&nbsp;
  <img alt="Node.js" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original.svg" />&nbsp;&nbsp;
  <img alt="TypeScript" width="50" height="50" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/typescript/typescript-original.svg" />
</p>

![poke-env](https://img.shields.io/badge/poke--env-0.12.1-3B4CCA?style=flat-square)
![Stable-Baselines3](https://img.shields.io/badge/Stable--Baselines3-2.7.1-9C27B0?style=flat-square)
![Gymnasium](https://img.shields.io/badge/Gymnasium-1.2.3-0081A5?style=flat-square)
![PettingZoo](https://img.shields.io/badge/PettingZoo-1.24.3-EF476F?style=flat-square)
![WebSockets](https://img.shields.io/badge/WebSockets-16.0-010101?style=flat-square)
![PPO](https://img.shields.io/badge/Reinforcement_Learning-PPO-FF6F00?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## Features

- Five ready-to-use bots with progressively more sophisticated decision-making
- Local bot-versus-bot battles on a private Pokémon Showdown server
- Round-robin cross-evaluation with tabulated results
- Direct battles between any two selected agents
- Public ladder support through a shared Pokémon Showdown account
- Generation 9 Random Battle support
- Matchup, damage, speed, status, boosts, abilities, hazards, and switching analysis
- Intelligent use of Terastallization and compatibility with Mega Evolution, Z-Moves, and Dynamax
- Team-role and battle-phase awareness in the competitive agent
- Minimal and advanced PPO reinforcement-learning environments
- Training, evaluation, batch testing, debug logging, and log-analysis utilities
- Pretrained and smoke-test model files included under `models/`

## Bots

### RandomBot

The baseline agent. It selects a legal action randomly through `poke-env`. It is useful as a control opponent when comparing other strategies or training an RL model.

### MaxDamageBot

Chooses the available move with the greatest raw base power. If a special battle mechanic is available, it uses it immediately alongside the selected attack. This bot provides a simple offensive baseline but does not account for accuracy, typing, status moves, switching, or long-term positioning.

### SimpleHeuristicsBot

Wraps the built-in `poke-env` `SimpleHeuristicsPlayer`. It considers basic type matchups, move power, setup opportunities, and switching, making it a stronger general-purpose baseline than purely random or raw-damage play.

### SmartBot

A custom tactical agent that assigns a value to every available action. Its evaluation includes expected damage, type effectiveness, STAB, accuracy, priority, speed, HP, boosts, status effects, abilities, entry hazards, matchup danger, and first-turn restrictions.

SmartBot also:

- Compares the immediate value of attacking with the future value of switching
- Detects urgent threats and likely knockouts
- Avoids unsafe switches by estimating entry-hazard damage
- Values setup, recovery, utility, buffs, and debuffs
- Selects special mechanics only when they offer a meaningful advantage

### CompetitiveBot

The most detailed rule-based agent. It builds a team plan, identifies each Pokémon's likely role, evaluates the battle phase, remembers recent actions, and scores moves and switches in context rather than as isolated choices.

Its strategy layer recognizes concepts such as hazard setting and removal, pivots, walls, breakers, cleaners, setup win conditions, recovery, screens, cleric support, phazing, anti-setup tools, item control, scouting, disruption, and predicted opponent switches. Debug output is enabled by default so its selected action and reasoning can be inspected after every turn.

### MiniRLBot

An educational PPO agent with a compact 12-value observation vector and four move-slot actions. It observes both active Pokémon's HP, move power, type multipliers, and fainted-team fractions. It learns to select attacks but does not directly learn switching decisions.

Default model: `models/mini_move_rl_agent.zip`

### AdvancedRLBot

A larger PPO agent that combines reinforcement learning with the project's competitive evaluation layer. It uses a 121-value observation vector and ten actions: four move slots plus six possible team slots.

The observation includes battle context, team survival, battle phase, matchup and threat scores, expected damage, move roles, accuracy, priority, status, speed advantage, switch safety, and entry-hazard penalties. Special mechanics are delegated to the same tactical selector used by the heuristic agents.

Default model: `models/advanced_rl_agent.zip`

> **Note:** The interactive `src/main.py` menu currently exposes RandomBot, MaxDamageBot, SimpleHeuristicsBot, SmartBot, and CompetitiveBot. The RL agents are operated through their dedicated training/evaluation scripts or imported programmatically.

## Requirements

- Python 3.10 or newer recommended
- Node.js and npm for local battles
- Git
- A Pokémon Showdown account only when playing on the public ladder

GPU acceleration is optional. PPO training works on CPU, although larger training runs can take considerably longer.

## Installation

From the `pokemon-showdown-ai` directory, create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Local Pokémon Showdown server

The repository is expected to sit next to a Pokémon Showdown checkout, as shown below. Install its Node.js dependencies before running local battles:

```text
Pokemon-Showdown-AI-Full-Project/
├── pokemon-showdown/
└── pokemon-showdown-ai/
```

```bash
cd ../pokemon-showdown
npm install
node pokemon-showdown start --no-security
```

The Python agents connect to:

- WebSocket: `ws://localhost:8000/showdown/websocket`
- Authentication endpoint: `http://localhost:8000/action.php?`

Keep the server terminal running while using local mode.

## Configuration

Create `config.json` in the project root. The file is required by the current configuration loader and is intentionally ignored by Git to protect credentials.

For local-only use, an empty ladder configuration is sufficient:

```json
{
  "ladder_account": {}
}
```

For public ladder play, provide one shared Pokémon Showdown account:

```json
{
  "ladder_account": {
    "username": "your_showdown_username",
    "password": "your_showdown_password"
  }
}
```

Only the selected ladder bot is created, so a single account is enough. Never commit `config.json` or publish your password.

## Usage

Run commands from the `pokemon-showdown-ai` directory.

```bash
python src/main.py
```

The interactive program first asks where the battles should run:

```text
Are you playing in local server (1) or ladder (2):
```

### Local mode

Local mode creates all five standard agents. Enter the number of battles and choose one of two result modes:

- **Table:** runs a round-robin cross-evaluation between every bot
- **Print:** lets you select two different bots and prints their victory counts

### Ladder mode

Ladder mode asks for a battle count and one bot. The selected agent logs into the official Pokémon Showdown server using `config.json`, searches for `gen9randombattle` matches, and prints rating information after completion.

Use ladder automation responsibly and comply with the Pokémon Showdown rules and server policies.

## Reinforcement Learning

All RL commands require the local Pokémon Showdown server to be running.

### Train the minimal agent

```bash
python tools/train_rl_agent.py --timesteps 20000 --opponent random
```

Available opponents are defined by the script. The output defaults to `models/mini_move_rl_agent.zip`; use `--output` to select another path.

```bash
python tools/train_rl_agent.py --timesteps 50000 --opponent max --output models/my_mini_agent.zip
```

### Evaluate the minimal agent

```bash
python tools/evaluate_rl_agent.py --battles 50 --opponents random max simple
```

Evaluate a custom model with `--model`:

```bash
python tools/evaluate_rl_agent.py --model models/my_mini_agent.zip --battles 100
```

### Train the advanced agent

```bash
python tools/train_advanced_rl_agent.py --timesteps 100000 --opponent max
```

Continue training from an existing PPO model with `--input`:

```bash
python tools/train_advanced_rl_agent.py --input models/advanced_rl_agent.zip --timesteps 100000 --output models/advanced_rl_agent_v2.zip
```

### Evaluate the advanced agent

```bash
python tools/evaluate_advanced_rl_agent.py --battles 50 --opponents random max simple competitive
```

## Testing and Log Analysis

Run a reproducible SmartBot-versus-CompetitiveBot batch and save all console output:

```bash
python tools/run_bot_batch.py --battles 20 --log debug_logs/batch.log
```

Include SmartBot's detailed diagnostics:

```bash
python tools/run_bot_batch.py --battles 20 --log debug_logs/batch.log --smart-debug
```

Analyze the generated competitive log:

```bash
python tools/analyze_competitive_logs.py debug_logs/batch.log
```

## Project Structure

```text
pokemon-showdown-ai/
├── models/                         # Trained PPO model archives
├── src/
│   ├── agents/                     # Rule-based and RL agents
│   ├── battle/                     # Shared battle evaluation utilities
│   ├── config/                     # Account configuration loader
│   ├── integrations/poke_env/      # poke-env login compatibility patch
│   ├── strategy/
│   │   ├── competitive/            # Team planning and action scoring
│   │   └── data/                   # Abilities, buffs, debuffs, and move effects
│   └── main.py                     # Interactive application entry point
├── tools/                          # Training, evaluation, batch, and analysis CLIs
├── config.json                    # Local credentials; ignored by Git
├── requirements.txt               # Pinned Python dependencies
└── LICENSE                        # MIT License
```

## Technology Stack

- **Python:** agents, battle logic, command-line interface, and training tools
- **poke-env:** Pokémon Showdown protocol, battle state, players, and environments
- **PyTorch:** neural-network backend
- **Stable-Baselines3:** PPO implementation and model persistence
- **Gymnasium and PettingZoo:** RL spaces and multi-agent environment interfaces
- **NumPy:** numerical observation vectors
- **Pandas:** structured experiment and analysis data
- **Matplotlib:** training and evaluation visualization support
- **WebSockets and Requests:** live server communication and authentication
- **Tabulate:** terminal result tables
- **Node.js and TypeScript:** the local Pokémon Showdown server and simulator

## Troubleshooting

### `FileNotFoundError: config.json`

Create `config.json` in the repository root using one of the examples in the [Configuration](#configuration) section.

### Connection refused on `localhost:8000`

Start the local Pokémon Showdown server and leave it running:

```bash
cd ../pokemon-showdown
node pokemon-showdown start --no-security
```

### RL model not found

Train the corresponding agent first or pass the correct archive using `--model`. Stable-Baselines3 model archives should remain as `.zip` files.

### Ladder authentication fails

Check the username and password in `config.json`. Public ladder play requires valid credentials, while local mode does not authenticate.

### PowerShell blocks virtual-environment activation

For the current PowerShell session, you can allow locally created scripts with:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

## Roadmap

- Add the RL agents to the interactive launcher
- Add automated tests and continuous integration
- Track benchmark results across agents and model versions
- Add configurable formats and server endpoints
- Improve opponent modelling and partial-information handling
- Add experiment metadata, checkpoints, and training visualizations

## Disclaimer

This is an independent educational project and is not affiliated with, endorsed by, or sponsored by Nintendo, Game Freak, The Pokémon Company, or the Pokémon Showdown team. Pokémon and all related names are trademarks of their respective owners.

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
