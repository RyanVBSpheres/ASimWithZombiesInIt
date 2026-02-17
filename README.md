# ASimWithZombiesInIt
Top Down Zombie Survival Sim

## Overview
A graphical simulation featuring a controllable player, wandering zombies, and other creatures in an environment with dynamic smell and sound emissions.

## Features
- **Controllable Player**: Navigate using arrow keys or WASD
- **Wandering Zombies**: Red entities that roam the environment
- **Wandering Creatures**: Green entities that move around
- **Smell Trails**: Entities leave smell trails behind them as they move
  - Player: Cyan smell
  - Zombies: Purple smell
  - Creatures: Orange smell
- **Sound Emissions**: Movement generates sounds that emanate from their source and fade with distance
  - Shown as expanding yellow rings
  - Generated when entities move a certain distance

## Installation

### Requirements
- Python 3.7+
- pygame
- numpy

### Setup
```bash
pip install -r requirements.txt
```

## Running the Simulation

### Quick Start (Unix/Linux/Mac)
```bash
./run.sh
```

### Manual Start
```bash
python simulation.py
```

Or with Python 3 explicitly:
```bash
python3 simulation.py
```

## Controls
- **Arrow Keys** or **WASD**: Move the player
- **ESC**: Quit the simulation

## How It Works

### Entity Types
- **Player** (Blue circle): Controlled by the user
- **Zombies** (Red circles): AI-controlled entities that wander randomly
- **Creatures** (Green circles): AI-controlled entities that wander more erratically

### Environmental Effects
- **Smells**: Persist in the environment where they are emitted, creating trails behind moving entities. They gradually decay over time.
- **Sounds**: Emanate from the position where they were generated (typically from movement). They expand outward as rings and fade with both distance and time.

## Technical Details
- **Resolution**: 1200x800 pixels
- **FPS**: 60 frames per second
- **Smell Decay Rate**: 0.995 per frame
- **Sound Decay Rate**: 0.92 per frame
- **Entities**: 8 zombies, 12 creatures, 1 player
