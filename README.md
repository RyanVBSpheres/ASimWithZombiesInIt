# ASimWithZombiesInIt
Top Down Zombie Survival Sim

## Overview
A graphical simulation featuring a controllable player, wandering zombies, and other creatures in an environment with dynamic smell and sound emissions. Zombies react to stimuli and chase the player!

## Features
- **Controllable Player**: Navigate using arrow keys or WASD
- **Reactive Zombies**: Red entities that react to player proximity, sounds, and smells
  - Chase player within detection range (200 pixels)
  - Follow sounds (150 pixel range)
  - Follow smell trails (100 pixel range, prefer player smell)
  - Wander randomly when no stimuli detected
- **Wandering Creatures**: Green entities that move around independently
- **Health & Agility System**: All entities have health and agility attributes
  - Player: Health 100, Agility 1.2 (more agile)
  - Zombies: Health 100, Agility 0.8 (less agile)
  - Creatures: Health 100, Agility 1.3 (most agile)
- **Smell Trails**: Entities leave smell trails behind them as they move
  - Player: Cyan smell rings
  - Zombies: Purple smell rings
  - Creatures: Orange smell rings
- **Sound Emissions**: Movement generates sounds that emanate from their source and fade with distance
  - Shown as expanding yellow rings
  - Generated when entities move a certain distance
- **Performance Optimized**: Runs at 60+ FPS with capped effects
  - Maximum 300 smells
  - Maximum 50 sounds

## Installation

### Requirements
- Python 3.7+
- pygame

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
- **Player** (Blue ring): Controlled by the user
- **Zombies** (Red rings): AI-controlled entities that react to stimuli and chase the player
- **Creatures** (Green rings): AI-controlled entities that wander independently

### Environmental Effects
- **Smells**: Persist in the environment where they are emitted, creating trails behind moving entities. They gradually decay over time.
- **Sounds**: Emanate from the position where they were generated (typically from movement). They expand outward as rings and fade with both distance and time.

### Zombie AI Behavior
Zombies use a priority-based stimulus system:
1. **Player Detection** (highest priority): Chase player if within 200 pixels
2. **Sound Attraction**: Follow nearby sounds within 150 pixels
3. **Smell Following**: Follow smell trails within 100 pixels (prefer player's cyan smell)
4. **Random Wandering** (default): Wander randomly when no stimuli detected

## Technical Details
- **Resolution**: 1200x800 pixels
- **FPS**: 60+ frames per second (optimized)
- **Entities**: 8 zombies, 12 creatures, 1 player
- **Visual Style**: Ring-based rendering for clarity and performance
- **Performance Caps**: 300 max smells, 50 max sounds
