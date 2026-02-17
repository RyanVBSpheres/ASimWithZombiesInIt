# ASimWithZombiesInIt
Top Down Zombie Survival Sim

## Overview

A zombie survival game with realistic predator mechanics for sound and smell tracking, along with character stats that affect gameplay. Control a player character to survive against zombies that hunt using sight, sound, and smell!

## 🎮 How to Play

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python game.py
```

### Controls
- **WASD** or **Arrow Keys**: Move your character
- **ESC**: Quit the game

### Objective
Survive as long as possible! Zombies will track you using smell (persistent, long-range) and sound (movement-based, short-range). Move strategically to avoid being caught!

## Key Features

### Graphical Interface
- **Real-time gameplay**: Smooth 30 FPS action
- **Visual feedback**: See your player (yellow), zombies (red), smell trails (green), and sound trails (blue)
- **Stats display**: Monitor health, agility, speed, and zombie count in real-time
- **Camera follows player**: The view stays centered on your character

### Character Stats
- **Health**: Character's current health (0-100)
- **Agility**: Determines movement speed; reduces proportionally with health loss
- **Strength**: Determines damage dealt in attacks

### Sound & Smell Mechanics

The simulation uses realistic predator tracking mechanics:

#### Sound System
- **Movement-based**: Sound is almost non-existent when characters are stationary
- **Speed-dependent**: Moving faster generates louder sounds
- **Fast decay**: Sound trails dissipate quickly (decay rate: 0.5)
- **Short range**: Effective detection range of ~10 units

#### Smell System
- **Always present**: Characters constantly emit scent regardless of movement
- **Persistent trails**: Smell lingers much longer than sound (decay rate: 0.1)
- **Long range**: Effective detection range of ~20 units (2x sound range)

#### Predator Tracking
Zombies use realistic predator behavior:
1. **Primary sense**: Smell (longer range, more persistent)
2. **Secondary sense**: Sound (shorter range, movement-based)
3. Zombies follow the strongest combined trail toward prey

### Combat & Damage
- Attacks deal damage based on attacker's strength stat
- Taking damage reduces health
- **Health loss reduces agility**: Characters become slower as they take damage
- Movement speed = agility / 10.0

## Files

- `game.py`: Graphical game interface (pygame)
- `character.py`: Character class with health, agility, and strength stats
- `trail_system.py`: Sound and smell trail mechanics
- `simulation.py`: Core simulation logic and text-based demo
- `test_simulation.py`: Comprehensive unit tests

## Running the Simulation (Text Mode)

If you want to run the text-based simulation instead of the graphical game:

### Run the demo:
```bash
python simulation.py
```

### Run tests:
```bash
python test_simulation.py
```

## Demo Output

The demo demonstrates:
1. Minimal sound when player is stationary
2. Sound and smell trail creation during movement
3. Smell persisting after movement stops
4. Agility and speed reduction from damage
5. Zombie tracking using combined sound/smell

## Implementation Details

### Trail Decay Rates
- Sound: 0.5 per tick (fast decay)
- Smell: 0.1 per tick (slow decay, 5x more persistent)

### Movement Speed Formula
```
move_speed = agility / 10.0
```

### Agility Reduction from Damage
```
agility = base_agility * (current_health / max_health)
```

### Sound Intensity When Moving
```
intensity = move_speed * 2.0  (if moving)
intensity = 0.05             (if stationary - almost non-existent)
```

### Trail Detection Range
- Sound: 10 units
- Smell: 20 units (2x sound range)

## Game Mechanics

1. **Player Movement**: Creates sound (when moving) and smell trails
2. **Trail Persistence**: Smell trails last ~5x longer than sound trails
3. **Zombie AI**: Zombies follow strongest trail (smell > sound priority)
4. **Combat**: Damage reduces health, which proportionally reduces agility
5. **Speed Penalty**: Lower agility = slower movement speed

## Testing

The test suite validates:
- Character stat initialization
- Movement speed based on agility
- Damage reducing health and agility
- Sound generation only when moving
- Smell always being generated
- Trail decay mechanics
- Zombie tracking behavior
- Combat damage dealing

All 23 tests pass successfully.
