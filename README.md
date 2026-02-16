# ASimWithZombiesInIt
Top Down Zombie Survival Sim

## Features

- **Circular Detection**: Player's sounds and smells emanate in circles rather than squares
- **Circular Entities**: All entities (player, zombies, animals) are represented as circles
- **Health System**: All sentient characters have health that can be damaged and restored
- **Animals (NPCs)**: Animals wander the world making sounds and smells that attract zombies
- **Zombie Eating Behavior**: When zombies are close to players or animals, they eat them, reducing victim health and increasing zombie health

## Installation

1. Install Python 3.12 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python simulation.py
```

## Controls

- **WASD** or **Arrow Keys**: Move the player
- **R**: Toggle visibility of sound/smell ranges
- **ESC**: Quit the simulation

## Game Mechanics

### Entities

- **Player (Blue Circle)**: You control this character. Emits sound and smell in circular ranges that attract zombies.
- **Zombies (Green Circles)**: Hunt players and animals by detecting sounds and smells. Will eat nearby victims.
- **Animals (Brown Circles)**: NPCs that wander randomly and emit sounds/smells that attract zombies.

### Health System

- Player starts with 100 health
- Zombies start with 80 health  
- Animals start with 50 health
- When a zombie is within eating range (15 pixels) of a victim, it eats them every second
- Each bite deals 5 damage to the victim and heals the zombie by 3 health
- When health reaches 0, the entity dies

### Circular Detection

- Sounds and smells emanate in perfect circles (Euclidean distance), not squares (Manhattan/Chebyshev distance)
- Player sound range: 150 pixels (red circle)
- Player smell range: 100 pixels (yellow circle)
- Animal sound range: 120 pixels
- Animal smell range: 80 pixels
- Zombies can detect and move toward any entity within these circular ranges

## Testing

Run the test suite to verify all features:

```bash
python -m unittest test_simulation -v
```

The tests verify:
- Circular distance calculations (not square-based)
- Health system for all entities
- Eating behavior and health changes
- Circular representation of entities
- Circular detection ranges

## Implementation Details

The simulation uses **Euclidean distance** (√((x₁-x₂)² + (y₁-y₂)²)) for all distance calculations, ensuring that:
1. Sound and smell propagate in circles
2. Zombie detection uses circular ranges
3. All entities are drawn as circles with defined radii
4. Eating range is also circular

This contrasts with square-based detection which would use Manhattan distance (|x₁-x₂| + |y₁-y₂|) or Chebyshev distance (max(|x₁-x₂|, |y₁-y₂|)).
